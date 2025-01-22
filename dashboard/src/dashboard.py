import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st
from datetime import datetime

from tasks import *

#Load cleaned data
df = detik_popular_news()
words = sentence_processing(df)
list_ = []
for word in words:
  article_count = filter_length(word, df)
  list_.append({'word contain': word,
                'article count': article_count})
  
df_ = pd.DataFrame(list_)

current_time = datetime.now()

# Detik popular news bar chart
sns.set(style='dark')
st.header('Detik Popular News Dashboard')
st.text('Scrapped on : %s' % current_time)

st.subheader('Most Frequent Words')
fig, ax = plt.subplots()
words = df_['word contain'] 
counts = df_['article count']
max_counts = df_['article count'].max()
bar_colors = ['midnightblue' if counts == max_counts else 'tab:blue' for counts in counts]
ax.bar(words, counts, color=bar_colors)
ax.set_ylabel('Article Count')
ax.set_title('Most Frequent Words in Detik Popular News')
st.pyplot(fig)

# Detik popular news data
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")

df_csv = convert_df(df)
st.download_button(
    label="Download detiknews popular data",
    data=df_csv,
    file_name="popular_dataset.csv",
    mime="text/csv",
)

st.subheader('Detiknews Indeks')
d = st.date_input("Choose news date index", value=current_time, format="MM/DD/YYYY")
d = d.strftime("%m/%d/%Y")

list_indeks = []
df_indeks = detik_news_indeks(d)
indeks_length = len(df_indeks)
words_indeks = sentence_processing(df_indeks)
for word_indeks in words_indeks:
  article_indeks_count = filter_length(word_indeks, df_indeks)
  list_indeks.append({'word contain': word_indeks,
                'article count': article_indeks_count})
  
df_indeks_ = pd.DataFrame(list_indeks)

st.subheader('Most Frequent Detiknews Indeks Words')
st.write("Total detiknews index article:", indeks_length)

fig, ax = plt.subplots()

indeks_words = df_indeks_['word contain'] 
indeks_counts = df_indeks_['article count']
max_indeks_counts = df_indeks_['article count'].max()

bar_colors = ['midnightblue' if indeks_counts == max_indeks_counts else 'tab:blue' for indeks_counts in indeks_counts]

ax.bar(indeks_words, indeks_counts, color=bar_colors)
ax.set_ylabel('Article Count')
ax.set_title('Most Frequent Words in Detiknews Indeks')

for bar in ax.patches:
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() / 2 + bar.get_y(),
            round(bar.get_height()), ha = 'center',
            color = 'w')
  
st.pyplot(fig)

df_indeks_csv = convert_df(df_indeks)
st.download_button(
    label="Download detiknews indeks data",
    data=df_indeks_csv,
    file_name="indeks_dataset.csv",
    mime="text/csv",
)