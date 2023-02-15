import streamlit as st 
import pandas as pd
import numpy as np

view = [100, 50 ,50]
view

# st.bar_chart(view)
st.text_input('hello')
st.write('hi')

st.dataframe( data = view )

##############################

import os
import sys
import urllib.request
import requests 
from ckonlpy.tag import Twitter
from collections import Counter
import numpy as np 
import pandas as pd
import re

###### api사용해서 불러오기 

client_id = "7BluQlzfnBbWg8ALRkpq"
client_secret = "ZTCPVEwdLc"
url = 'https://openapi.naver.com/v1/search/news.json'



# display_num : 한 번에 표시할 검색 결과 개수(기본값: 10, 최댓값: 100)
def Keword( key, display_num):
      # keyword = key
      headers = { 'X-Naver-Client-Id': client_id
                , 'X-Naver-Client-Secret': client_secret}
      params = {'query': key
                , 'display':display_num
                ,'sort': 'sim' }

      r = requests.get(url, params = params, headers = headers).json()['items']

      return r 


## 데이터프레임에 나눠담기
def info(places):
    PubDate = []
    Title = []
    Link = [] 
    Description = []

    for place in places:

        PubDate.append(place['pubDate'])
        Title.append(place['title'])
        Link.append(place['originallink'])      
        Description.append(place['description'])
         

    ar = np.array([PubDate, Title, Link, Description ]).T
    dtf = pd.DataFrame(ar, columns=['PubDate', 'Title', 'Link', 'Description' ])

    return dtf


####가져오기 

search = Keword('신종보이스피싱수법',100)
news = info(search) 



# 기본 정제 
def basic_clear(text):
    for i in range(len(text)) : 
        text[i] = text[i].replace('<b>', '')
        text[i] = text[i].replace('</b>', '')
        text[i] = text[i].replace('&apos;', '') 
        text[i] = text[i].replace('&quot;', '') 
    return text

basic_clear(news['Title'])
basic_clear(news['Description'])


## 중복 타이틀 제거
for i in range(99):
        if news['Title'].iloc[i][:8] == news['Title'].iloc[i+1][:8]:
             news['Title'].iloc[i] = np.NaN
news.dropna(inplace=True)
news.info()

import datetime


# 날짜형으로 형변환

news['PubDate'] = pd.to_datetime(news['PubDate'], format='%a, %d %b %Y  %H:%M:%S', exact=False) # 수정완료!

# news['PubDate'] = 
news['PubDate'] = news['PubDate'].dt.strftime('%m.%d') # 수정완료!



################### 빈도체크########

# 특수기호 제거 
def extract_word(text):
    hangul = re.compile('[^가-힣]') 
    result = hangul.sub(' ', text) 
    return result

for i in range (len(news['Title'])):
    news['Title'].iloc[i] = extract_word(news['Title'].iloc[i])
    news['Description'].iloc[i] = extract_word(news['Description'].iloc[i])
    

# 리스트형으로 변환 
title = news['Title']
description = news['Description']

from collections import Counter
import re
from konlpy.tag import Okt 

okt = Okt()


def news_words_list(news_title) :
    news_words = []

    for j in news_title:
      a = okt.morphs(j)
    
      for i in a:
          news_words.append(i)

    return news_words



## 제목과 본문 합치기
title = news_words_list(title)
description = news_words_list(description)
title.extend(description)


## 1글자 제거
drop_one_words = [x for x in title if len(x)>1 ]

with open('stopwords.txt', 'r',encoding = 'cp949') as f:
    list_file = f.readlines()
stopwords = list_file[0].split(",")

final_words = [x for x in drop_one_words if x not in stopwords]


# 데이터프레임으로 변환
df = pd.DataFrame(final_words, columns = ['words'])


# # 빈도측정 
frequent = Counter(final_words).most_common()
df = pd.DataFrame(frequent, columns=['keyword','count'])

df.sort_values(by=['count'], ascending = False)

df['rank'] = df['count'].rank(method='first', ascending = False)
df['rank'] = df['rank'].astype(int)
# .rank(axis=0, method='min', ascending=True)

df = df[['rank','keyword']]
df.columns = ['랭킹','실시간 관련 키워드']
df.set_index('랭킹',inplace = True)

# df.set_index('rank',inplace = True)
st.dataframe(data = df.head(3))



########################
## 순서변경

search = Keword('신종보이스피싱수법',100)
news = info(search) 



# 기본 정제 
def basic_clear(text):
    for i in range(len(text)) : 
        text[i] = text[i].replace('<b>', '')
        text[i] = text[i].replace('</b>', '')
        text[i] = text[i].replace('&apos;', '') 
        text[i] = text[i].replace('&quot;', '') 
    return text

basic_clear(news['Title'])
basic_clear(news['Description'])


## 중복 타이틀 제거
for i in range(99):
        if news['Title'].iloc[i][:8] == news['Title'].iloc[i+1][:8]:
             news['Title'].iloc[i] = np.NaN
news.dropna(inplace=True)
news.info()

import datetime


# 날짜형으로 형변환

news['PubDate'] = pd.to_datetime(news['PubDate'], format='%a, %d %b %Y  %H:%M:%S', exact=False) # 수정완료!

# news['PubDate'] = 
news['PubDate'] = news['PubDate'].dt.strftime('%m.%d') # 수정완료!



a = news[['PubDate','Title','Link']].head(5)

st.write('관련 뉴스')
for i in range(len(a['Title'])):
    txt='{date}    [{txt}]({link})'.format(date =  a['PubDate'][i], txt = a['Title'][i], link = a['Link'][i])
    st.write(txt) 


##########################















st.dataframe(a)
url_a = 'https://www.donga.com/news/Society/article/all/20230210/117824734/2'
url_b = 'http://www.kado.net/news/articleView.html?idxno=1168786'

a_link = st.multiselect("choose a link", [url_a])
text='check out this제발 [link]({link})'.format(link = url_a)
st.markdown(a_link ,unsafe_allow_html=True)


txt = st.text_area('Text to analyze', '''
    It was the best of times, it was the worst of times, it was
    the age of wisdom, it was the age of foolishness, it was
    the epoch of belief, it was the epoch of incredulity, it
    was the season of Light, it was the season of Darkness, it
    was the spring of hope, it was the winter of despair, (...)
    ''')


st.write("check out this [link](https://share.streamlit.io/mesmith027/streamlit_webapps/main/MC_pi/streamlit_app.py)")


st.write(a['Link'][0])

st.write(' df')

st.write(a['Title'][0])

for i in a['Title'] :
    st.write(i,"[.](a['Link'][0])") 
    
st.write("[a['Title'][0]](a['Link'][0])")




view = [[100, 50 ]
        ,[1,2] ,
       ['df','dfd']]

st.dataframe( data = view )




a_link = 'https://www.donga.com/news/Society/article/all/20230210/117824734/2'
txt='[{txt}]({link})'.format(txt='text', link = a_link)
# st.write(txt)
st.write()


for i in view[2] :
    st.write(i[0])
    st.write(i[1])
    
st.write(a)
    
cc = pd.DataFrame()
for i in range(len(a['Title'])):
    txt='{date}    [{txt}]({link})'.format(date =  a['PubDate'][i], txt = a['Title'][i], link = a['Link'][i])
    st.write(txt) 
    
    # st.write(a['Link'][i])
    
    

st.dataframe( data = cc )