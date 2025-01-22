import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st
from datetime import datetime

from detikscraper import *

# Detik popular news data
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")

current_time = datetime.now()

st.subheader('Detiknews Search')
start_date = st.date_input("Choose start date", value=current_time)
end_date = st.date_input("Choose end date", value=current_time)

start_date, end_date = start_date.strftime("%d/%m/%Y"), end_date.strftime("%d/%m/%Y")

query = st.text_input("Keywords", value=None)

df = scrape_detik(query, start_date, end_date)
st.write('Total articles: %s' % len(df))
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

df_indeks = detik_news_indeks(d)
st.write('Total articles: %s' % len(df_indeks))
df_indeks_csv = convert_df(df_indeks)
st.download_button(
    label="Download detiknews indeks data",
    data=df_indeks_csv,
    file_name="detik_indeks_dataset.csv",
    mime="text/csv",
)