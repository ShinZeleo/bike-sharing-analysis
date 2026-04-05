import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_style("whitegrid")

base_path = os.path.dirname(__file__)

# load data
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

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.title("Dashboard Analisis Bike Sharing")
st.markdown("Dashboard ini menjawab pertanyaan bisnis terkait pola penyewaan sepeda berdasarkan musim, cuaca, dan waktu.")

# filter di sidebar
st.sidebar.header("Filter Data")

# filter Tanggal
min_date = df['dteday'].min().date()
max_date = df['dteday'].max().date()

start_date = st.sidebar.date_input(
    "Tanggal Mulai",
    value=min_date,
    min_value=min_date,
    max_value=max_date
)

end_date = st.sidebar.date_input(
    "Tanggal Akhir",
    value=max_date,
    min_value=min_date,
    max_value=max_date
)

# validasi input tanggal
if start_date > end_date:
    st.sidebar.warning("Tanggal mulai tidak boleh lebih besar dari tanggal akhir!")
    st.stop()

# filter Musim
season_options = sorted(df['season'].unique())
season_filter = st.sidebar.multiselect(
    "Pilih Musim",
    options=season_options,
    default=season_options
)

# filter Cuaca
weather_options = sorted(df['weathersit'].unique())
weather_filter = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca",
    options=weather_options,
    default=weather_options
)

# validasi input filter
if not season_filter:
    st.sidebar.warning("Pilih minimal satu musim!")
    st.stop()

if not weather_filter:
    st.sidebar.warning("Pilih minimal satu kondisi cuaca!")
    st.stop()

# tampilkan filter
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
    st.warning("Tidak ada data yang sesuai dengan filter. Silakan ubah filter!")
    st.stop()

# mertic
st.sidebar.markdown("---")
st.sidebar.write(f"Jumlah data terfilter: **{len(filtered_df)}**")

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("Total Penyewaan", f"{int(filtered_df['cnt'].sum()):,}")
col_m2.metric("Rata-rata Harian", f"{int(filtered_df['cnt'].mean()):,}")
col_m3.metric("Maksimum", f"{int(filtered_df['cnt'].max()):,}")
col_m4.metric("Minimum", f"{int(filtered_df['cnt'].min()):,}")

st.markdown("---")

# "Bagaimana perbandingan jumlah penyewaan sepeda antar musim pada tahun 2012?"
st.header("Pertanyaan 1: Perbandingan Penyewaan Antar Musim")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Rata-rata Penyewaan Berdasarkan Musim")
    season_df = filtered_df.groupby('season')['cnt'].mean().reset_index()
    season_df.columns = ['Musim', 'Rata-rata Penyewaan']

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    bars = sns.barplot(x='Musim', y='Rata-rata Penyewaan', data=season_df, ax=ax, hue='Musim', palette=colors, legend=False)

    ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Musim", fontsize=14, fontweight='bold')
    ax.set_xlabel("Musim", fontsize=12)
    ax.set_ylabel("Rata-rata Jumlah Penyewaan", fontsize=12)

    for bar in bars.patches:
        bars.annotate(f'{int(bar.get_height()):,}',
                      (bar.get_x() + bar.get_width() / 2., bar.get_height()),
                      ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader("Insight")
    if not season_df.empty:
        max_season = season_df.loc[season_df['Rata-rata Penyewaan'].idxmax(), 'Musim']
        min_season = season_df.loc[season_df['Rata-rata Penyewaan'].idxmin(), 'Musim']
        st.success(f"Musim **{max_season}** memiliki rata-rata penyewaan **tertinggi**.")
        st.error(f"Musim **{min_season}** memiliki rata-rata penyewaan **terendah**.")

    st.subheader(" Rekomendasi")
    st.info(
        "- **Disarankan** meningkatkan ketersediaan dan distribusi sepeda pada musim gugur (Fall).\n"
        "- **Perlu dilakukan** strategi promosi khusus di musim semi (Spring) untuk mendorong penyewaan.\n"
        "- **Strategi yang dapat diterapkan**: paket diskon musiman untuk meningkatkan penggunaan di musim sepi."
    )

st.markdown("---")

# "Sejauh mana kondisi cuaca memengaruhi jumlah penyewaan sepeda harian selama tahun 2012?"
st.header("Pertanyaan 2: Pengaruh Cuaca terhadap Penyewaan")

col3, col4 = st.columns([2, 1])

with col3:
    st.subheader("Rata-rata Penyewaan Berdasarkan Kondisi Cuaca")
    weather_df = filtered_df.groupby('weathersit')['cnt'].mean().reset_index()
    weather_df.columns = ['Kondisi Cuaca', 'Rata-rata Penyewaan']

    fig, ax = plt.subplots(figsize=(8, 5))
    colors_w = ['#FFD93D', '#6BCB77', '#4D96FF']
    bars = sns.barplot(x='Kondisi Cuaca', y='Rata-rata Penyewaan', data=weather_df, ax=ax,
                       hue='Kondisi Cuaca', palette=colors_w[:len(weather_df)], legend=False)

    ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca", fontsize=14, fontweight='bold')
    ax.set_xlabel("Kondisi Cuaca", fontsize=12)
    ax.set_ylabel("Rata-rata Jumlah Penyewaan", fontsize=12)

    for bar in bars.patches:
        bars.annotate(f'{int(bar.get_height()):,}',
                      (bar.get_x() + bar.get_width() / 2., bar.get_height()),
                      ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.tight_layout()
    st.pyplot(fig)

with col4:
    st.subheader("Insight")
    if not weather_df.empty:
        max_w = weather_df.loc[weather_df['Rata-rata Penyewaan'].idxmax(), 'Kondisi Cuaca']
        min_w = weather_df.loc[weather_df['Rata-rata Penyewaan'].idxmin(), 'Kondisi Cuaca']
        st.success(f"Cuaca **{max_w}** menghasilkan penyewaan **tertinggi**.")
        st.error(f"Cuaca **{min_w}** menghasilkan penyewaan **terendah**.")

    st.subheader("Rekomendasi")
    st.info(
        "- **Disarankan** mengintegrasikan data prakiraan cuaca ke sistem operasional untuk memprediksi demand.\n"
        "- **Perlu dilakukan** pengurangan unit aktif saat cuaca buruk untuk efisiensi pemeliharaan.\n"
        "- **Strategi yang dapat diterapkan**: penawaran indoor activity partnerships saat cuaca buruk."
    )

st.markdown("---")

# "Bagaimana perbandingan tren jam sibuk penyewaan sepeda antara hari kerja dan hari libur?"
st.header(" Pertanyaan 3: Tren Jam Sibuk — Hari Kerja vs Hari Libur")

col5, col6 = st.columns([2, 1])

with col5:
    st.subheader("Perbandingan Pola Penyewaan per Jam (Working Day vs Holiday)")

    if not filtered_hour.empty:
        hour_plot = filtered_hour.copy()
        hour_plot['workingday'] = hour_plot['workingday'].map({0: 'Hari Libur', 1: 'Hari Kerja'})

        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=hour_plot, x='hr', y='cnt', hue='workingday',
                     marker='o', ax=ax, palette=['#FF6B6B', '#4ECDC4'])

        ax.set_title("Perbandingan Penyewaan Sepeda per Jam\n(Hari Kerja vs Hari Libur)",
                      fontsize=14, fontweight='bold')
        ax.set_xlabel("Jam", fontsize=12)
        ax.set_ylabel("Rata-rata Jumlah Penyewaan", fontsize=12)
        ax.set_xticks(range(0, 24))
        ax.legend(title='Tipe Hari', fontsize=10)

        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("Tidak ada data hour untuk rentang tanggal yang dipilih.")

with col6:
    st.subheader("Insight")
    st.markdown("""
    **Hari Kerja:**
    - Terdapat **dua puncak utama**: jam 08.00 (berangkat kerja) dan jam 17.00–18.00 (pulang kerja)

    **Hari Libur:**
    - Pola penyewaan **lebih merata** dengan puncak di **siang hari** (10.00–15.00)
    """)

    st.subheader("Rekomendasi")
    st.info(
        "- **Disarankan** menambah unit sepeda di jam commuting (08.00 & 17.00) pada hari kerja.\n"
        "- **Perlu dilakukan** redistribusi sepeda lebih awal pada hari libur ke area rekreasi.\n"
        "- **Strategi yang dapat diterapkan**: penyesuaian jadwal maintenance di luar jam sibuk."
    )

st.markdown("---")

# distribusi penyewaan
st.header("Analisis Tambahan: Distribusi Penyewaan")

fig, ax = plt.subplots(figsize=(10, 4))
sns.histplot(filtered_df['cnt'], bins=30, ax=ax, color='#45B7D1', edgecolor='white')
ax.set_title("Distribusi Jumlah Penyewaan Sepeda Harian", fontsize=14, fontweight='bold')
ax.set_xlabel("Jumlah Penyewaan", fontsize=12)
ax.set_ylabel("Frekuensi", fontsize=12)
plt.tight_layout()
st.pyplot(fig)
