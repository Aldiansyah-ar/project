import requests
import pandas as pd
from bs4 import BeautifulSoup
import string 
import re
import nltk
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk import word_tokenize
from nltk.probability import FreqDist

try:
  pass
except:
  nltk.download('punkt_tab')

def detik_popular_news():
  url = f'https://www.detik.com/terpopuler/news'
  data = []
  text = requests.get(url).text
  soup = BeautifulSoup(text, 'lxml')
  articles_container = soup.find_all('article', class_='list-content__item')
  for article in articles_container:
    headline = article.find('div', 'media__text').find('a').text
    link = article.find('div', 'media__text').find('a')['href']
    data.append({'source': 'Detiknews',
                'title': headline,
                'link': link})

  df = pd.DataFrame(data)
  return df

def sentence_processing(df):
  # Sentence
  sentence = df['title'].to_list()
  sentence = ' '.join(sentence)

  # Sentence processing
  lowercase_sentence = sentence.lower()
  lowercase_sentence = re.sub(r"\d+", "", lowercase_sentence)
  lowercase_sentence = lowercase_sentence.translate(str.maketrans("","",string.punctuation))
  lowercase_sentence = lowercase_sentence.strip()

  # Stemming process
  stemmer_factory = StemmerFactory()
  stemmer = stemmer_factory.create_stemmer()
  stemmer_sentence = stemmer.stem(lowercase_sentence)

  # Remove whitespace leading & trailing
  stopword_factory = StopWordRemoverFactory()
  stopword = stopword_factory.create_stop_word_remover()
  stopword_sentence = stopword.remove(stemmer_sentence)
  tokens = nltk.tokenize.word_tokenize(stopword_sentence)

  # Frequent words
  frequent = nltk.FreqDist(tokens)
  most_common = frequent.most_common(5)

  most_common_list = []
  for x in most_common:
    most_common_list.append(x[0])
  
  return most_common_list

def filter_length(word, df):
  pattern = rf'\b\w*{word}\w*\b'
  df_filtered = df['title'].apply(lambda x: x.lower())
  df_filtered = df_filtered.str.contains(pattern, regex=True, case=False)
  df_filtered = df['title'].loc[df_filtered == True]
  article_count = len(df_filtered)

  return article_count

def detik_indeks_page(date):
  url = f'https://news.detik.com/berita/indeks?page=1&date={date}'
  text = requests.get(url).text
  sop = BeautifulSoup(text, 'lxml')
  try:
    paging = sop.find_all('div','pagination text-center mgt-16 mgb-16')[0].find_all('a')[-2]
    last_page = paging.text
  except:
    last_page = 1
  return last_page

def detik_news_indeks(date):
    last_page = detik_indeks_page(date)
    data = []
    for page in range(1,int(last_page)+1):
        url = f'https://news.detik.com/berita/indeks?page={page}&date={date}'
        text = requests.get(url).text
        soup = BeautifulSoup(text, 'lxml')
        articles_container = soup.find_all('article', class_='list-content__item')
        for article in articles_container:
            headline = article.find('div', 'media__text').find('a').text
            link = article.find('div', 'media__text').find('a')['href']
            data.append({'source': 'Detiknews',
                         'title': headline,
                         'url': link,
                         'date': date})

    df = pd.DataFrame(data)
    return df