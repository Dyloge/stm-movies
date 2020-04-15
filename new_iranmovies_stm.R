options(prompt = "R> ", continue = "+", width = 70, useFancyQuotes = FALSE)

###################
# Required packages
###################
library("stm")
library("wordcloud")
library("RColorBrewer")
library("reticulate")
###################
# Reading data
###################
data <- read.csv("C:/Users/amir/Documents/DTM_Iranian_Cinema/final_data/all_categories_movies.csv")
###################
# Preprocessing
###################
set.seed(2138)
processed <- textProcessor(data$documents, metadata = data)
out <- prepDocuments(processed$documents, processed$vocab, processed$meta)
docs <- out$documents
vocab <- out$vocab
meta  <-out$meta
plotRemoved(processed$documents, lower.thresh = seq(1, 200, by = 100))
###################
# Fitting the model
###################
out <- prepDocuments(processed$documents, processed$vocab,
                     processed$meta, lower.thresh = 15)
shortdoc <- substr(out$meta$documents, 1, 200)
shortdocname <- substr(out$meta$docname, 1, 200)
###################
# Using the content covariate
###################
iranmoviePrevFit <- stm(documents = out$documents, vocab = out$vocab,
                        K = 20, prevalence =~ rating + s(year), 
                        max.em.its = 75,
                        data = out$meta, init.type = "Spectral")
###################
# Model selection
###################
iranmoviesSelect <- selectModel(out$documents, out$vocab, K = 20,
                                prevalence =~ rating + s(year), 
                                max.em.its = 75,
                                data = out$meta, runs = 20, seed = 8458159)
selectedmodel <- iranmoviesSelect$runout[[3]]
###################
# Describing model
###################
out$meta$rating <- as.numeric(out$meta$rating)
prep <- estimateEffect(1:20 ~ rating + s(year), iranmoviePrevFit,
                       meta = out$meta, uncertainty = "Global")
summary(prep, topics=3)

estimateEffect(formula = 1:20 ~ rating + s(year), stmobj = iranmoviePrevFit,
               metadata = out$meta, uncertainty = "Global")
###################
# Visualizing
###################
for(i in 1:20) {
   thoughts <- paste("thoughts", i, sep = "")
   thoughtsshortdocname <- paste("thoughtsshortdocname", i, sep = "")
   mostrel <- findThoughts(iranmoviePrevFit, texts = shortdoc, n = 1,
                           topics = i)$docs[[1]]
   mostrelname <-findThoughts(iranmoviePrevFit, texts = shortdocname, n = 1,
                              topics = i)$docs[[1]]
   assign(thoughtsshortdocname,mostrelname)
   assign(thoughts, mostrel)
   Titr <- paste("Topic",i, sep = " ")
   plotpdfs <- paste(i,".pdf", sep = "")
####################
   #Producing Pdfs
###################
   pdf(plotpdfs)
   par(mar=c(2,2,1,1))
   layout(mat = matrix(c(1,2,4,1,3,5), ncol=2),
          heights = c(0.25, 1, 1), widths = c(2, 2 , 2)) 
   plot.new()
   text(0.5,0.5,Titr,cex=2,font=2)
   plot(prep, covariate = "year", topics = i, 
        model = selectedmodel, method = "continuous",
        printlegend = FALSE,
        xaxt="n",bty="n", xlab = "release date of Iranian movies",
        ylab = "Topic proportion",linecol = "blue")
   yearnames <- out$meta$release_date
   axis(1,
        at = as.numeric(yearnames) - min(as.numeric(yearnames)),
        labels = yearnames)
   cloud(iranmoviePrevFit, topic = i,random.order=FALSE, 
         rot.per=0.35,colors=brewer.pal(8, "Dark2"),
         scale = c(4, 1), max.words=150)
   plotQuote(c(mostrel,mostrelname), width = 30, text.cex = 1.5)
   plot(iranmoviePrevFit, type = "labels",width = 40, text.cex = 1.5,
        topics = i)
   dev.off()
####################
   #Moving outputs to directory
###################
   my.file.rename <- function(from, to) {
      todir <- dirname(to)
      if (!isTRUE(file.info(todir)$isdir)) dir.create(todir, recursive=TRUE)
      file.rename(from = from,  to = to)
   }
   
   my.file.rename(from = paste("C:/Users/amir/Documents/",plotpdfs, sep = ""),
                  to = paste("C:/Users/amir/Documents/DTM_Iranian_Cinema/output_plots/",plotpdfs, sep = ""))
}



