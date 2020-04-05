from bs4 import BeautifulSoup
import requests
import csv
count=0
csv_file = open('chef101.csv' , 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Recipe_id','Recipe_name','Recipe_url','recipe_image'])
with open('breakfast.html') as html_file :
    soup = BeautifulSoup(html_file , 'lxml')
for match in soup.find_all('a',class_ = "grd-tile-link"):
    count=count+1
    link = match['href']
    title = match['title']
    '''for link in range(0,18):
        source = requests.get(link).text
        soup2 = BeautifulSoup(source, 'lxml')
        ingredients = soup2.find('div',class_ ="entry-details recipe-ingredients").text
        csv_writer.writerow([ingredients])'''
    for pic in match.find_all('img'):
        img = pic.get('data-src', 'n/a') 
    csv_writer.writerow([count,title,link,img])
csv_file.close()






csv_file = open('chef102.csv' , 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Recipe_id','Recipe_name','Recipe_url','recipe_image'])

with open('desserts.html') as html_file :
    soup = BeautifulSoup(html_file , 'lxml')
for match in soup.find_all('a',class_ = "grd-tile-link"):
    count=count+1
    link = match['href']
    title = match['title']
    '''for link in range(0,18):
        source = requests.get(link).text
        soup2 = BeautifulSoup(source, 'lxml')
        ingredients = soup2.find('div',class_ ="entry-details recipe-ingredients").text
        csv_writer.writerow([ingredients])'''
    for pic in match.find_all('img'):
        img = pic.get('data-src', 'n/a') 
    csv_writer.writerow([count,title,link,img])
csv_file.close()







csv_file = open('chef103.csv' , 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Recipe_id','Recipe_name','Recipe_url','recipe_image'])

with open('lunch.html') as html_file :
    soup = BeautifulSoup(html_file , 'lxml')
for match in soup.find_all('a',class_ = "grd-tile-link"):
    count=count+1
    link = match['href']
    title = match['title']
    '''for link in range(0,18):
        source = requests.get(link).text
        soup2 = BeautifulSoup(source, 'lxml')
        ingredients = soup2.find('div',class_ ="entry-details recipe-ingredients").text
        csv_writer.writerow([ingredients])'''
    for pic in match.find_all('img'):
        img = pic.get('data-src', 'n/a') 
    csv_writer.writerow([count,title,link,img])
csv_file.close()





csv_file = open('chef104.csv' , 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Recipe_id','Recipe_name','Recipe_url','recipe_image'])

with open('dinner.html') as html_file :
    soup = BeautifulSoup(html_file , 'lxml')
for match in soup.find_all('a',class_ = "grd-tile-link"):
    count=count+1
    link = match['href']
    title = match['title']
    '''for link in range(0,18):
        source = requests.get(link).text
        soup2 = BeautifulSoup(source, 'lxml')
        ingredients = soup2.find('div',class_ ="entry-details recipe-ingredients").text
        csv_writer.writerow([ingredients])'''
    for pic in match.find_all('img'):
        img = pic.get('data-src', 'n/a') 
    csv_writer.writerow([count,title,link,img])
csv_file.close()



csv_file = open('chef105.csv' , 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Recipe_id','Recipe_name','Recipe_url','recipe_image'])

with open('drink.html') as html_file :
    soup = BeautifulSoup(html_file , 'lxml')
for match in soup.find_all('a',class_ = "grd-tile-link"):
    count=count+1
    link = match['href']
    title = match['title']
    '''for link in range(0,18):
        source = requests.get(link).text
        soup2 = BeautifulSoup(source, 'lxml')
        ingredients = soup2.find('div',class_ ="entry-details recipe-ingredients").text
        csv_writer.writerow([ingredients])'''
    for pic in match.find_all('img'):
        img = pic.get('data-src', 'n/a') 
    csv_writer.writerow([count,title,link,img])
csv_file.close()

