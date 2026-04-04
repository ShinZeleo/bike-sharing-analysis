import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_style("whitegrid")

base_path = os.path.dirname(__file__)

# ambil data
df = pd.read_csv(os.path.join(base_path, 'main_data.csv'))
hour_df = pd.read_csv(os.path.join(base_path, '../data/hour.csv'))

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

st.title("Dashboard Analisis Bike Sharing")

# filter data
st.sidebar.header("Filter Data")

season_filter = st.sidebar.multiselect(
    "Pilih Musim",
    options=df['season'].unique(),
    default=df['season'].unique()
)

weather_filter = st.sidebar.multiselect(
    "Pilih Cuaca",
    options=df['weathersit'].unique(),
    default=df['weathersit'].unique()
)

filtered_df = df[
    (df['season'].isin(season_filter)) &
    (df['weathersit'].isin(weather_filter))
]

st.sidebar.write("Jumlah data:", len(filtered_df))

col_m1, col_m2, col_m3 = st.columns(3)

col_m1.metric("Total Penyewaan", int(filtered_df['cnt'].sum()))
col_m2.metric("Rata-rata", int(filtered_df['cnt'].mean()))
col_m3.metric("Maksimum", int(filtered_df['cnt'].max()))

# distribusi & musim 
col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribusi Penyewaan")
    fig, ax = plt.subplots(figsize=(5,3))
    sns.histplot(filtered_df['cnt'], bins=30, ax=ax)
    ax.set_xlabel("Jumlah Penyewaan")
    ax.set_ylabel("Frekuensi")
    st.pyplot(fig)

with col2:
    st.subheader("Rata-rata Berdasarkan Musim")
    season_df = filtered_df.groupby('season')['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(5,3))
    sns.barplot(x='season', y='cnt', data=season_df, ax=ax)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata")
    st.pyplot(fig)

# cuaca & jam
col3, col4 = st.columns(2)

with col3:
    st.subheader("Rata-rata Berdasarkan Cuaca")
    weather_df = filtered_df.groupby('weathersit')['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(5,3))
    sns.barplot(x='weathersit', y='cnt', data=weather_df, ax=ax)
    ax.set_xlabel("Cuaca")
    ax.set_ylabel("Rata-rata")
    st.pyplot(fig)

with col4:
    st.subheader("Pola Penyewaan per Jam")
    hour_group = hour_df.groupby('hr')['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(6,3))
    sns.lineplot(x='hr', y='cnt', data=hour_group, marker='o', ax=ax)
    ax.set_xticks(range(0,24))
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-rata")
    st.pyplot(fig)