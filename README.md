# Bike Sharing Data Analysis

## Deskripsi Proyek

Proyek ini bertujuan untuk menganalisis pola penggunaan layanan bike sharing berdasarkan beberapa faktor seperti musim, kondisi cuaca, dan waktu (jam). Analisis dilakukan untuk memahami perilaku pengguna serta faktor-faktor yang memengaruhi jumlah penyewaan sepeda.

Dataset yang digunakan merupakan dataset Bike Sharing yang berisi data penyewaan sepeda harian dan per jam.

## Pertanyaan Bisnis

Beberapa pertanyaan yang ingin dijawab melalui analisis ini:

1. Bagaimana perbandingan jumlah penyewaan sepeda antar musim pada tahun 2012?
2. Sejauh mana kondisi cuaca memengaruhi jumlah penyewaan sepeda harian selama tahun 2012?
3. Bagaimana perbandingan tren jam sibuk penyewaan sepeda antara hari kerja dan hari libur dalam 12 bulan terakhir?

## Insight Utama

- Musim gugur (Fall) memiliki rata-rata penyewaan tertinggi, sedangkan musim semi (Spring) paling rendah.
- Cuaca cerah menghasilkan jumlah penyewaan tertinggi, sedangkan kondisi cuaca buruk menurunkan minat pengguna.
- Terdapat dua puncak waktu penyewaan pada hari kerja, yaitu pagi hari sekitar pukul 08.00 dan sore hari sekitar pukul 17.00–18.00. Pada hari libur, pola penyewaan lebih merata dengan puncak di siang hari.
- Temperatur memiliki korelasi positif terhadap jumlah penyewaan, sedangkan kelembapan dan kecepatan angin cenderung berdampak negatif.

## Struktur Proyek

```
submission/
│
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv
│
├── data/
│   ├── day.csv
│   └── hour.csv
│
├── Proyek_Analisis_Data.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Setup Environment

### Menggunakan Conda

```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install --upgrade pip
pip install -r requirements.txt
```

### Menggunakan Pipenv

```bash
pipenv install
pipenv shell
pip install --upgrade pip
pip install -r requirements.txt
```

## Cara Menjalankan Dashboard

1. Pastikan semua dependencies sudah terinstall:

```bash
pip install -r requirements.txt
```

2. Jalankan Streamlit:

```bash
streamlit run dashboard/dashboard.py
```

## Deployment

Dashboard dapat diakses melalui:

[\[link-streamlit\]](https://bike-sharing-analysis-zell.streamlit.app/)

## Catatan

Proyek ini dibuat sebagai bagian dari submission analisis data dengan tujuan memahami pola penggunaan layanan bike sharing secara sederhana namun informatif.
