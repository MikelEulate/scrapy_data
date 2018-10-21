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

pages = [str(i) for i in range(1,5)]
years_url = [str(i) for i in range(2014,2018)]

# Preparing the monitoring of the loop
start_time = time()
requests = 0

# For every year in the interval 2000-2017
for year_url in years_url:

    # For every page in the interval 1-4
    for page in pages:

        # Make a get request
        response = get('http://www.imdb.com/search/title?release_date=' + year_url + 
        '&sort=num_votes,desc&page=' + page)

        # Pause the loop
        sleep(randint(8,15))

        # Monitor the requests
        requests += 1
        elapsed_time = time() - start_time
        print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
        clear_output(wait = True)

        # Throw a warning for non-200 status codes
        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))

        # Break the loop if the number of requests is greater than expected
        if requests > 72:
            warn('Number of requests was greater than expected.')  
            break 

        # Parse the content of the request with BeautifulSoup
        page_html = BeautifulSoup(response.text, 'html.parser')
        movie_containers = page_html.find_all('div', class_ = 'lister-item mode-advanced')
        for container in movie_containers:

        	print('Name: ', container.h3.a.text)
        	name.append(container.h3.a.text)

        	first_year = container.h3.find('span', class_ = 'lister-item-year text-muted unbold').get_text()
        	year.append(first_year.replace('(', '').replace(')', ''))

        	first_rate = container.find('div', class_ = 'inline-block ratings-imdb-rating').get_text()
        	rate.append(first_rate.replace('\n', ''))

        	first_votes = container.find('span', attrs = {'name': 'nv'})['data-value']
        	votes.append(first_votes)

        	description_f = container.find_all('p',  class_ = 'text-muted')[1].text.replace('\n', '').replace('\t', ' ')
        	description.append(description_f)

        	genre_f = container.find('span',  class_ = 'genre').text
        	genre.append(genre_f)

        	minutes_f = container.find('span',  class_ = 'runtime').text.split(' min')[0]
        	minutes.append(minutes_f)

        	director_f = container.find_all('p')[-2].a.text
        	director.append(director_f)





df = pd.DataFrame({'movie': name,
                       'year': year,
                       'rate': rate,
                       'votes': votes,
                       'description': description,
                       'genre': genre, 
                       'minutes': minutes, 
                       'director': director
                       })

print(df.head())
df.to_csv('../data/imbd_2014_2018.csv')
