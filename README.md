# Bike Sharing Data Analysis

## Deskripsi Proyek

Proyek ini bertujuan untuk menganalisis pola penggunaan layanan bike sharing berdasarkan beberapa faktor seperti musim, kondisi cuaca, dan waktu (jam). Analisis dilakukan untuk memahami perilaku pengguna serta faktor-faktor yang memengaruhi jumlah penyewaan sepeda.

Dataset yang digunakan merupakan dataset Bike Sharing yang berisi data penyewaan sepeda harian dan per jam.

## Pertanyaan Bisnis

Beberapa pertanyaan yang ingin dijawab melalui analisis ini:

1. Apakah ada musim tertentu yang membuat penyewaan sepeda lebih ramai dari biasanya?
2. Sejauh mana kondisi cuaca memengaruhi jumlah penyewa sepeda harian?
3. Pada jam berapa saja penyewaan sepeda biasanya mencapai puncaknya?

## Insight Utama

- Musim gugur (Fall) memiliki rata-rata penyewaan tertinggi, sedangkan musim semi (Spring) paling rendah.
- Cuaca cerah menghasilkan jumlah penyewaan tertinggi, sedangkan kondisi cuaca buruk menurunkan minat pengguna.
- Terdapat dua puncak waktu penyewaan, yaitu pagi hari sekitar pukul 08.00 dan sore hari sekitar pukul 17.00–18.00.
- Temperatur memiliki korelasi positif terhadap jumlah penyewaan, sedangkan kelembapan dan kecepatan angin cenderung berdampak negatif.

## Struktur Proyek

```
submission/
│
├── dashboard/
│ ├── dashboard.py
│ └── main_data.csv
│
├── data/
│ ├── day.csv
│ └── hour.csv
│
├── Proyek_Analisis_Data.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Cara Menjalankan Dashboard

1. Pastikan semua dependencies sudah terinstall:

```
    pip install -r requirements.txt
```

2. Jalankan Streamlit:

```
    streamlit run dashboard/dashboard.py
```

## Deployment

Dashboard dapat diakses melalui:

[\[link-streamlit\]](https://bike-sharing-analysis-zell.streamlit.app/)

## Catatan

Proyek ini dibuat sebagai bagian dari submission analisis data dengan tujuan memahami pola penggunaan layanan bike sharing secara sederhana namun informatif.
