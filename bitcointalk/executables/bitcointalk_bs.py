
# pip install six
from datetime import datetime
from six.moves.urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_posts():
    url = 'https://bitcointalk.org/index.php?topic=4631576.0'
    html = requests.get(url)
    #print(html)
    soup = BeautifulSoup(html.content, 'html.parser')
    rows = soup.select('#bodyarea .windowbg, #bodyarea .windowbg2')
    for row in rows:
        user = row.select('.poster_info b a')[0].contents
        time = row.select('.td_headerandpost table .smalltext')[0].contents
        message = row.select('.post')[0].contents
        #user_f = row.select('.poster_info b a')[0].contents
        #user = user_f[0]
        #print(user[0])
        grade_t = row.find('td', class_ = 'poster_info').find('div', class_ = 'smalltext').text.replace('\n', '').replace('\t', ' ')
        #print(str(grade))

        grade = grade_t.split('       ')[1].strip()
        #print(grade)
        try: 
            activity = grade_t.split('Activity: ')[1].split(' Merit:')[0]
        except:
            activity = ''
        #print(activity)
        try:
            merit = grade_t.split(' Merit: ')[1]
        except:
            merit = ''
        #print(merit)

        #message = row.select('.post')[0].contents
        #print(message[0])





        if (user == time == message):
            continue

        user = str(user[0])

        time = time[0]
        time = time if not hasattr(time, 'contents') else time.contents[0]
        #time = datetime.strptime(str(time), '%b %d, %Y, %I:%M:%S %p')

        message = [str(content) for content in message]

        yield {'user': user, 'time': time, 'grade': grade, 'activity': activity, 'merit': merit, 'message': message}

if __name__ == '__main__':
    print(list(get_posts()))

    df = pd.DataFrame(get_posts())
    print(df.head())
    df.to_csv('../data/bitcointalk_final.csv')
