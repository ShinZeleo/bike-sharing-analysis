import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings

warnings.filterwarnings('ignore', category=FutureWarning)
sns.set_style("white")

base_path = os.path.dirname(__file__)

# ===== LOAD DATA =====
try:
    df = pd.read_csv(os.path.join(base_path, 'main_data.csv'))
    hour_df = pd.read_csv(os.path.join(base_path, '../data/hour.csv'))
    df['dteday'] = pd.to_datetime(df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
except FileNotFoundError as e:
    st.error(f"File data tidak ditemukan: {e}")
    st.stop()
except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat data: {e}")
    st.stop()

# ===== PAGE CONFIG =====
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.title("Dashboard Analisis Bike Sharing")
st.markdown("Dashboard ini menjawab pertanyaan bisnis terkait pola penyewaan sepeda berdasarkan musim, cuaca, dan waktu.")

# ===== SIDEBAR FILTERS =====
st.sidebar.header("Filter Data")

min_date = df['dteday'].min().date()
max_date = df['dteday'].max().date()

start_date = st.sidebar.date_input(
    "Tanggal Mulai", value=min_date, min_value=min_date, max_value=max_date
)
end_date = st.sidebar.date_input(
    "Tanggal Akhir", value=max_date, min_value=min_date, max_value=max_date
)

if start_date > end_date:
    st.sidebar.warning("Rentang tanggal tidak valid. Tanggal mulai harus sebelum tanggal akhir.")
    st.stop()

season_options = sorted(df['season'].unique())
season_filter = st.sidebar.multiselect("Pilih Musim", options=season_options, default=season_options)

weather_options = sorted(df['weathersit'].unique())
weather_filter = st.sidebar.multiselect("Pilih Kondisi Cuaca", options=weather_options, default=weather_options)

user_type = st.sidebar.selectbox("Tipe Pengguna", options=['Semua', 'Casual', 'Registered'])

if not season_filter:
    st.sidebar.warning("Pilih minimal satu musim.")
    st.stop()
if not weather_filter:
    st.sidebar.warning("Pilih minimal satu kondisi cuaca.")
    st.stop()

# ===== APPLY FILTERS =====
try:
    filtered_df = df[
        (df['season'].isin(season_filter)) &
        (df['weathersit'].isin(weather_filter)) &
        (df['dteday'] >= pd.to_datetime(start_date)) &
        (df['dteday'] <= pd.to_datetime(end_date))
    ]
    filtered_hour = hour_df[
        (hour_df['dteday'] >= pd.to_datetime(start_date)) &
        (hour_df['dteday'] <= pd.to_datetime(end_date))
    ]
except Exception as e:
    st.warning(f"Terjadi kesalahan saat memfilter data: {e}")
    st.stop()

if filtered_df.empty:
    st.warning("Tidak ada data yang sesuai dengan filter. Silakan ubah filter.")
    st.stop()

# Pilih kolom berdasarkan tipe pengguna
if user_type == 'Casual':
    cnt_col = 'casual'
elif user_type == 'Registered':
    cnt_col = 'registered'
else:
    cnt_col = 'cnt'

# ===== METRICS =====
st.sidebar.markdown("---")
st.sidebar.write(f"Jumlah data terfilter: **{len(filtered_df)}**")

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("Total Penyewaan", f"{int(filtered_df[cnt_col].sum()):,}")
col_m2.metric("Rata-rata Harian", f"{int(filtered_df[cnt_col].mean()):,}")
col_m3.metric("Maksimum", f"{int(filtered_df[cnt_col].max()):,}")
col_m4.metric("Minimum", f"{int(filtered_df[cnt_col].min()):,}")

st.markdown("---")

# ===== PERTANYAAN 1 =====
st.header("Pertanyaan 1: Perbandingan Penyewaan Antar Musim")

col1, col2 = st.columns([2, 1])

with col1:
    season_df = filtered_df.groupby('season')[cnt_col].mean().reset_index()
    season_df.columns = ['Musim', 'Rata-rata Penyewaan']

    colors = ['#4ECDC4'] * len(season_df)
    colors[season_df['Rata-rata Penyewaan'].idxmax()] = '#FF6B6B'

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(season_df['Musim'], season_df['Rata-rata Penyewaan'], color=colors)

    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                f"{int(bar.get_height()):,}",
                ha='center', va='bottom', fontsize=9)

    ax.set_title("Perbandingan Rata-rata Penyewaan Sepeda Antar Musim", fontsize=14, fontweight='bold')
    ax.set_xlabel("Musim", fontsize=12)
    ax.set_ylabel("Rata-rata Jumlah Penyewaan", fontsize=12)
    ax.grid(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader("Insight")
    if not season_df.empty:
        max_season = season_df.loc[season_df['Rata-rata Penyewaan'].idxmax(), 'Musim']
        min_season = season_df.loc[season_df['Rata-rata Penyewaan'].idxmin(), 'Musim']
        st.info(f"Musim **{max_season}** memiliki rata-rata penyewaan **tertinggi**.")
        st.warning(f"Musim **{min_season}** memiliki rata-rata penyewaan **terendah**.")

    st.caption("Pola ini menunjukkan bahwa musim gugur memberikan kondisi optimal untuk aktivitas bersepeda.")

    st.subheader("Rekomendasi")
    st.info(
        "- Disarankan meningkatkan ketersediaan sepeda pada musim dengan demand tertinggi.\n"
        "- Perlu dilakukan strategi promosi khusus di musim sepi.\n"
        "- Strategi yang dapat diterapkan: paket diskon musiman."
    )

st.markdown("---")

# ===== PERTANYAAN 2 =====
st.header("Pertanyaan 2: Pengaruh Cuaca terhadap Penyewaan")

col3, col4 = st.columns([2, 1])

with col3:
    weather_df = filtered_df.groupby('weathersit')[cnt_col].mean().reset_index()
    weather_df.columns = ['Kondisi Cuaca', 'Rata-rata Penyewaan']

    w_colors = ['#4ECDC4'] * len(weather_df)
    w_colors[weather_df['Rata-rata Penyewaan'].idxmax()] = '#FF6B6B'

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(weather_df['Kondisi Cuaca'], weather_df['Rata-rata Penyewaan'], color=w_colors)

    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                f"{int(bar.get_height()):,}",
                ha='center', va='bottom', fontsize=9)

    ax.set_title("Pengaruh Kondisi Cuaca terhadap Rata-rata Penyewaan Sepeda", fontsize=14, fontweight='bold')
    ax.set_xlabel("Kondisi Cuaca", fontsize=12)
    ax.set_ylabel("Rata-rata Jumlah Penyewaan", fontsize=12)
    ax.grid(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)

with col4:
    st.subheader("Insight")
    if not weather_df.empty:
        max_w = weather_df.loc[weather_df['Rata-rata Penyewaan'].idxmax(), 'Kondisi Cuaca']
        min_w = weather_df.loc[weather_df['Rata-rata Penyewaan'].idxmin(), 'Kondisi Cuaca']
        st.info(f"Cuaca **{max_w}** menghasilkan penyewaan **tertinggi**.")
        st.warning(f"Cuaca **{min_w}** menghasilkan penyewaan **terendah**.")

    st.caption("Cuaca cerah menjadi faktor utama yang mendorong pengguna untuk menyewa sepeda.")

    st.subheader("Rekomendasi")
    st.info(
        "- Disarankan mengintegrasikan data prakiraan cuaca untuk memprediksi demand.\n"
        "- Perlu dilakukan pengurangan unit aktif saat cuaca buruk untuk efisiensi.\n"
        "- Strategi yang dapat diterapkan: indoor activity partnerships saat cuaca buruk."
    )

st.markdown("---")

# ===== PERTANYAAN 3 =====
st.header("Pertanyaan 3: Tren Jam Sibuk — Hari Kerja vs Hari Libur")

col5, col6 = st.columns([2, 1])

with col5:
    if not filtered_hour.empty:
        hour_plot = filtered_hour.groupby(['hr', 'workingday'])['cnt'].mean().reset_index()
        hour_plot['workingday'] = hour_plot['workingday'].map({0: 'Hari Libur', 1: 'Hari Kerja'})

        fig, ax = plt.subplots(figsize=(10, 5))
        for label, group in hour_plot.groupby('workingday'):
            color = '#FF6B6B' if label == 'Hari Kerja' else '#4ECDC4'
            ax.plot(group['hr'], group['cnt'], label=label, color=color, linewidth=2)

        ax.set_title("Tren Penyewaan Sepeda per Jam: Hari Kerja vs Hari Libur",
                     fontsize=14, fontweight='bold')
        ax.set_xlabel("Jam", fontsize=12)
        ax.set_ylabel("Rata-rata Jumlah Penyewaan", fontsize=12)
        ax.set_xticks(range(0, 24))
        ax.legend(title='Tipe Hari', fontsize=10)
        ax.grid(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("Tidak ada data untuk rentang tanggal yang dipilih.")

with col6:
    st.subheader("Insight")
    st.markdown(
        "**Hari Kerja:** Dua puncak utama pada jam 08.00 dan 17.00-18.00 (pola commuting).\n\n"
        "**Hari Libur:** Pola lebih merata dengan puncak di siang hari 10.00-15.00 (pola rekreasi)."
    )

    st.caption("Perbedaan pola ini mengindikasikan bahwa sepeda digunakan untuk tujuan yang berbeda pada hari kerja dan hari libur.")

    st.subheader("Rekomendasi")
    st.info(
        "- Disarankan menambah unit sepeda di jam commuting pada hari kerja.\n"
        "- Perlu dilakukan redistribusi sepeda ke area rekreasi pada hari libur.\n"
        "- Strategi yang dapat diterapkan: penyesuaian jadwal maintenance di luar jam sibuk."
    )

st.markdown("---")
st.caption("Dashboard ini dibuat sebagai bagian dari submission proyek analisis data Bike Sharing.")
