from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep, time
from random import randint
from warnings import warn
from IPython.core.display import clear_output



name = []
year = []
rate = []
votes = []
description = []
genre = []
minutes = [] 
director = []



url = 'https://bitcointalk.org/index.php?topic=4631576.0'

response = get(url)
html_soup = BeautifulSoup(response.text, 'html.parser')
#print(type(html_soup))

pages = html_soup.find('td', class_ = 'middletext').find_all('a', class_ = 'navPages')#start_page= pages[0].text
last_page= pages[-2].text

start_ref = str(pages[0]).split('href="')[-1].split('"')[0]
last_ref = str(pages[-2]).split('href="')[-1].split('"')[0]


print('OK')
print(start_ref)
print(last_ref) 


#container = html_soup.find_all('div')[1].find_all('table', class_ = 'bordercolor')[0].find('tbody')
#cont = html_soup.find_all('div')[1].find_all('td', class_ = 'wPZXkyxtaytbpNdPSOhJgw')
#print(len(cont))
#print(cont)
rows = html_soup.select('#bodyarea .windowbg, #bodyarea .windowbg2')
#print(rows)
row = rows[0]

user = row.select('.poster_info b a')[0].contents
print(user[0])

grade = row.find('td', class_ = 'poster_info').find('div', class_ = 'smalltext').text.replace('\n', '').replace('\t', ' ')#.replace('       ', ' ')
#print(str(grade))

g = grade.split('       ')[1].strip()
print(g)

activity = grade.split('Activity: ')[1].split(' Merit:')[0]
print(activity)

merit = grade.split(' Merit: ')[1]
print(merit)

message = row.select('.post')[0].contents
print(message[0])
#for row in rows:
#        user = row.select('.poster_info b a')[0].contents
#        print(user[0])
