import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep, time
from random import randint
from warnings import warn
from IPython.core.display import clear_output


url_orig = 'https://bitcointalk.org/index.php?topic=4631576.0'


def get_posts(url):
    #url = 'https://bitcointalk.org/index.php?topic=4631576.0'
    html = requests.get(url)
    #print(html)
    soup = BeautifulSoup(html.content, 'html.parser')
    rows = soup.select('#bodyarea .windowbg, #bodyarea .windowbg2')
    for row in rows:
        user = row.select('.poster_info b a')[0].contents
        time = row.select('.td_headerandpost table .smalltext')[0].contents
        message = row.select('.post')[0].contents

        grade_t = row.find('td', class_ = 'poster_info').find('div', class_ = 'smalltext').text.replace('\n', '').replace('\t', ' ')
        grade = grade_t.split('       ')[1].strip()
        try: 
            activity = grade_t.split('Activity: ')[1].split(' Merit:')[0]
        except:
            activity = ''
        try:
            merit = grade_t.split(' Merit: ')[1]
        except:
            merit = ''

        #message = row.select('.post')[0].contents
        #print(message[0])

        if (user == time == message):
            continue

        user = str(user[0])

        time = time[0]
        time = time if not hasattr(time, 'contents') else time.contents[0]
        #time = datetime.strptime(str(time), '%b %d, %Y, %I:%M:%S %p')

        message = [str(content) for content in message]
        #message = message[0]

        yield {'user': user, 'time': time, 'grade': grade, 'activity': activity, 'merit': merit, 'message': message}


if __name__ == '__main__':



	response_orig = requests.get(url_orig)
	html_soup_orig = BeautifulSoup(response_orig.text, 'html.parser')

	pages = html_soup_orig.find('td', class_ = 'middletext').find_all('a', class_ = 'navPages')

	df = pd.DataFrame()

	for i in range(0,len(pages)-1):
		#print(i)
		url = str(pages[i]).split('href="')[-1].split('"')[0]

		print(url)
		#response = get(url)  

		#page_html = BeautifulSoup(response.text, 'html.parser')
		#container = page_html.find_all()
		#or element in container:
		df_i = pd.DataFrame(get_posts(url))
		df = df.append(df_i)
	print(df.head())
	df.to_csv('../data/bitcointalk_allposts.csv')


    	

