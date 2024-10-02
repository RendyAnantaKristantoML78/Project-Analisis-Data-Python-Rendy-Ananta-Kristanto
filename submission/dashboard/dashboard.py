import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Judul dan deskripsi dashboard saya
st.title('Dashboard Visualisasi Data Sewa Sepeda Harian')
st.markdown(
    """
    Nama: Rendy Ananta Kristanto<br>
    Email Dicoding: 71220840@students.ukdw.ac.id<br>
    Username Dicoding: @rendyanantakristanto<br>     
    """, 
    unsafe_allow_html=True
)

# Upload dataset day.csv dalam url dari github saya
day_df = pd.read_csv("https://raw.githubusercontent.com/RendyAnantaKristantoML78/Project-Analisis-Data-Python-Rendy-Ananta-Kristanto/refs/heads/main/submission/dashboard/day.csv")
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Mendapatkan rentang tanggal dari dataset, untuk menyiapkan range date
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

# Widget sidebar untuk memilih range date
with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu', 
        min_value=min_date, 
        max_value=max_date, 
        value=[min_date, max_date]
    )

# Filter data berdasarkan range date yang dipilih oleh pengguna
filtered_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & (day_df['dteday'] <= pd.to_datetime(end_date))]

# Perbandingan Jumlah Sewa Sepeda pada Hari Libur dan Hari Kerja
st.subheader('Perbandingan Jumlah Sewa Sepeda pada Hari Libur dan Hari Kerja')

holiday_sum_df = filtered_df[filtered_df['holiday'] == 1]['cnt']
workingday_sum_df = filtered_df[filtered_df['holiday'] == 0]['cnt']

plt.figure(figsize=(10, 6))
plt.plot(holiday_sum_df.values, label='Hari Libur', color='red')
plt.plot(workingday_sum_df.values, label='Hari Kerja', color='green')

plt.title('Perbandingan Jumlah Sewa Sepeda pada Hari Libur dan Hari Kerja')
plt.xlabel('Index Hari')
plt.ylabel('Jumlah Sewa Sepeda')

plt.legend()
st.pyplot(plt)

# Boxplot Perbandingan Jumlah Sewa Sepeda Hari Libur dan Hari Kerja
st.subheader('Boxplot Perbandingan Jumlah Sewa Sepeda Hari Libur dan Hari Kerja')

plt.figure(figsize=(10, 6))
sns.boxplot(x='holiday', y='cnt', data=filtered_df, palette='Set2')

plt.title('Perbandingan Jumlah Sewa Sepeda pada Hari Libur dan Hari Kerja')
plt.xlabel('Hari (0 = Workingday, 1 = Holiday)')
plt.ylabel('Jumlah Sewa Sepeda')

st.pyplot(plt)

# Perbandingan Total Jumlah Sewa Sepeda Berdasarkan Kondisi Cuaca dan Musim
st.subheader('Perbandingan Total Jumlah Sewa Sepeda Berdasarkan Kondisi Cuaca dan Musim')

weather_season_grouped = filtered_df.groupby(['weathersit', 'season'])['cnt'].sum().unstack()

plt.figure(figsize=(10, 6))
weather_season_grouped.plot(kind='bar')

plt.title('Perbandingan Total Jumlah Sewa Sepeda Berdasarkan Kondisi Cuaca dan Musim', fontsize=14)
plt.xlabel('Kondisi Cuaca (1: Clear, 2: Mist, 3: Light Snow/Light Rain)', fontsize=12)
plt.ylabel('Total Jumlah Sewa Sepeda', fontsize=12)

plt.legend(title='Musim (1: Spring, 2: Summer, 3: Fall, 4: Winter)', fontsize=10)
plt.grid(True)

st.pyplot(plt)

# Line plot Perbandingan Total Jumlah Sewa Sepeda Berdasarkan Kondisi Cuaca dan Musim
st.subheader('Line Plot Total Jumlah Sewa Sepeda Berdasarkan Kondisi Cuaca dan Musim')

def musim(season):
    if season == 1:
        return 'Spring'
    elif season == 2:
        return 'Summer'
    elif season == 3:
        return 'Fall'
    elif season == 4:
        return 'Winter'
    return None

plt.figure(figsize=(10, 6))
for season in weather_season_grouped.columns:
    plt.plot(weather_season_grouped.index, weather_season_grouped[season], marker='o', label=f'{musim(season)}')

plt.title('Perbandingan Total Jumlah Sewa Sepeda Berdasarkan Kondisi Cuaca dan Musim', fontsize=14)
plt.xlabel('Kondisi Cuaca (1: Clear, 2: Mist, 3: Light Snow/Light Rain)', fontsize=12)
plt.ylabel('Total Jumlah Sewa Sepeda', fontsize=12)

plt.legend(title='Musim', fontsize=10)
plt.grid(True)
plt.xticks(weather_season_grouped.index)

st.pyplot(plt)

# Menampilkan kesimpulan dari analisis
st.subheader('Kesimpulan')
st.markdown(
    """
    - Terdapat perbedaan yang signifikan, yang dimana jumlah sewa sepeda lebih tinggi di hari kerja daripada di hari libur, ini menandakan masih banyak orang yang datang kerja / melakukan aktifitas dengan menggunakan sepeda, sehingga dalam konteks bisnis, jumlah profit sewa sepeda akan lebih besar saat hari kerja.
    
    - Terdapat perbedaan juga, yang dimana jumlah sewa sepeda tertinggi adalah saat cuaca cerah di musim gugur, dan yang paling rendah keseluruhan adalah di cuaca salju ringan / hujan ringan. Jadi perusahaan dapat mempertimbangkan untuk menyewakan sepeda lebih banyak di cuaca cerah dan musim gugur karena banyak orang yang menyewa sepeda di saat tersebut.
    """
)

# Menampilkan data yang difilter dari range date
st.subheader('Data yang Difilter Berdasarkan Rentang Waktu')
st.write(filtered_df)

# Menampilkan data raw dari sumber
st.subheader('Dataset raw day.csv')
st.write(day_df)
