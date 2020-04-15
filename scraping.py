###################
# Importing required libraries
###################
from bs4 import BeautifulSoup
import requests
import csv
from csv import reader
import shutil
import os
###################
# Making output directories
###################
destination1 = 'C:/Users/amir/Documents/DTM_Iranian_Cinema/scraped_data'
destination2 = 'C:/Users/amir/Documents/DTM_Iranian_Cinema/final_data'
if not os.path.exists(destination1):
    os.mkdir(destination1)
if not os.path.exists(destination2):
    os.mkdir(destination2)
###################
# Opening csv file
###################
csv_file1 = open('cicinema_scraped_rawdata.csv',
                 'w', encoding='utf_8', newline='')
csv_writer = csv.writer(csv_file1)
csv_writer.writerow(['documents', 'docname',
                     'rating', 'release_date'])
###################
# Scraping data
###################
for page in range(1, 366):
    source = requests.get(
        'https://cicinema.com/en/movies?per_page=24&page=' + format(page)).text
    soup = BeautifulSoup(source, 'lxml')

    for movies in soup. find_all('div', class_='mv-item-infor'):
        documents = movies.find('p', class_='describe').text
        movie_name = movies.h6.a.span.text
        categories = movies.find_all('p')[2].text

        docname = movie_name.split('(')[0]
        date = movie_name.split('(')[1]
        release_date = date.split(')')[0]
        rating = categories. split(':')[1:][0]
        csv_writer.writerow([documents, docname,
                             rating, release_date])
csv_file1.close()
shutil.copy('cicinema_scraped_rawdata.csv',
            destination1)
os.remove('cicinema_scraped_rawdata.csv')
###################
# Reversing output csv file
###################
csv_file1 = open(destination1+'/cicinema_scraped_rawdata.csv',
                 'r+', encoding='utf_8', newline='')
csv_file2 = open('cicinema_scraped_rawdata_reverse.csv',
                 'w', encoding='utf_8', newline='')
csv_writer = csv.writer(csv_file2)
csv_writer.writerow(['documents', 'docname',
                     'rating', 'release_date'])
csv_reader1 = csv.reader(csv_file1)
next(csv_reader1)
for row in reversed(list(csv_reader1)):
    csv_writer.writerow(row)
csv_file1.close()
csv_file2.close()
shutil.copy('cicinema_scraped_rawdata_reverse.csv',
            destination1)
os.remove('cicinema_scraped_rawdata_reverse.csv')
###################
# Correcting non-digit and non-year values in release_date column
###################
r = csv.reader(
    open(destination1+'/cicinema_scraped_rawdata_reverse.csv', 'r+', encoding='utf_8'))
lines = list(r)
csv_file3 = open('cicinema_scraped_rawdata_reverse_correct.csv',
                 'w', encoding='utf_8', newline='')
csv_writer = csv.writer(csv_file3)
csv_writer.writerow(['documents', 'docname',
                     'rating', 'release_date'])
for i in range(1, len(lines)):
    if not lines[i][3].isdigit() or int(lines[i][3]) < 1900:
        i = i + 1
        if lines[i][3].isdigit() and int(lines[i][3]) > 1900:
            csv_writer.writerow([lines[i][0], lines[i][1],
                                 lines[i][2], lines[i][3]])
    else:
        csv_writer.writerow([lines[i][0], lines[i][1],
                             lines[i][2], lines[i][3]])
csv_file3.close()
csv_file2.close()
shutil.copy('cicinema_scraped_rawdata_reverse_correct.csv',
            destination1)
os.remove('cicinema_scraped_rawdata_reverse_correct.csv')
###################
# Indexing data
###################
f = csv.reader(
    open(destination1+'/cicinema_scraped_rawdata_reverse_correct.csv', 'r+', encoding='utf_8'))
flines = list(f)
csv_file4 = open('all_categories.csv',
                 'w', encoding='utf_8', newline='')
csv_writer = csv.writer(csv_file4)
csv_writer.writerow(['index', 'documents', 'docname',
                     'rating', 'release_date'])
indexf = 1
for k in range(1, len(flines)):
    csv_writer.writerow([indexf, flines[k][0], flines[k][1],
                         flines[k][2], flines[k][3]])
    indexf += 1
csv_file3.close()
csv_file4.close()
shutil.copy('all_categories.csv',
            destination1)
os.remove('all_categories.csv')
###################
# Producing seperate csv files according to movie categories(here annotated as ratig)
###################
c = csv.reader(open(
    destination1+'/all_categories.csv', 'r', encoding='utf_8'))
newlines = list(c)
cats = ["Feature", "Documentary", "Short Film",
        "Experimental", "Animation", "Video Clip", "Music Video"]
for j in cats:
    csv_file_j = open(j+'.csv', 'w', encoding='utf_8', newline='')
    csv_writer = csv.writer(csv_file_j)
    csv_writer.writerow(['index', 'documents', 'docname',
                         'rating', 'release_date'])
    index = 1
    for x in range(1, len(newlines)):
        if j in newlines[x][3]:
            csv_writer.writerow([index, newlines[x][1], newlines[x][2],
                                 newlines[x][3], newlines[x][4]])
            index += 1
    csv_file_j.close()
    shutil.copy(j+'.csv',
                destination1)
    os.remove(j+'.csv')
csv_file4.close()
###################
# Adding year cloumn
###################
p = ["all_categories", "Feature", "Documentary", "Short Film",
     "Experimental", "Animation", "Video Clip", "Music Video"]
for d in p:
    c = csv.reader(open(
        destination1 + '/' + d + '.csv', 'r+', encoding='utf_8'))
    newlines = list(c)
    csv_file_d = open(d+'_movies.csv', 'w', encoding='utf_8', newline='')
    csv_writer = csv.writer(csv_file_d)
    csv_writer.writerow(['index', 'documents', 'docname',
                         'rating', 'year', 'release_date'])
    for x in range(1, len(newlines)):
        year = int(newlines[x][4]) - 1979
        csv_writer.writerow([newlines[x][0], newlines[x][1], newlines[x][2],
                             newlines[x][3],  year, newlines[x][4]])
    csv_file_d.close()
    shutil.copy(d+'_movies.csv',
                destination2)
    os.remove(d+'_movies.csv')
csv_file4.close()
