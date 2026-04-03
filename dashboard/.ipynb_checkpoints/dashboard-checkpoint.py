import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
# ambil data
df = pd.read_csv('dashboard/main_data.csv')
hour_df = pd.read_csv('data/hour.csv')

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.title("Dashboard Analisis Bike Sharing")

# distribusi & musim 
col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribusi Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(5,3))
    sns.histplot(df['cnt'], bins=30, ax=ax)
    ax.set_xlabel("Jumlah Penyewaan")
    ax.set_ylabel("Frekuensi")
    st.pyplot(fig)

with col2:
    st.subheader("Rata-rata Penyewaan Berdasarkan Musim")
    season_df = df.groupby('season')['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(5,3))
    sns.barplot(x='season', y='cnt', data=season_df, ax=ax)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)

# cuaca & jam
col3, col4 = st.columns(2)

with col3:
    st.subheader("Rata-rata Penyewaan Berdasarkan Cuaca")
    weather_df = df.groupby('weathersit')['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(5,3))
    sns.barplot(x='weathersit', y='cnt', data=weather_df, ax=ax)
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)

with col4:
    st.subheader("Pola Penyewaan Berdasarkan Jam")
    hour_group = hour_df.groupby('hr')['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(6,3))
    sns.lineplot(x='hr', y='cnt', data=hour_group, marker='o', ax=ax)
    ax.set_xticks(range(0,24))
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)