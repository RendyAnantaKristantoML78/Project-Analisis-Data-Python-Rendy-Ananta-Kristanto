import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ssl
import urllib.request

ssl._create_default_https_context = ssl._create_unverified_context

#Gathering data

@st.cache_data
def load_data():
    day_df_path = "dashboard\day.csv"

    with urllib.request.urlopen(day_df_path) as response:
        day_df = pd.read_csv(response)

    return day_df


try:
    day_df = load_data()
except Exception as exception:
    st.error(f"Kesalahan saat memuat data: {exception}")
    st.stop()

#Visualisasi Data dan EDA

st.title('Dashboard Analisis Dataset Penyewaan Sepeda Dalam Harian')



#
holiday_sum_df = day_df[day_df['holiday'] == 1]['cnt']
workingday_sum_df = day_df[day_df['holiday'] == 0]['cnt']

plt.figure(figsize=(10, 6))
plt.plot(holiday_sum_df, label='Hari Libur', color='red', marker='o')
plt.plot(workingday_sum_df, label='Hari Kerja', color='green', marker='o')

plt.title('Perbandingan Jumlah Sewa Sepeda pada Hari Libur dan Hari Kerja')
plt.xlabel('Statistik Deskriptif')
plt.ylabel('Jumlah Sewa Sepeda')

plt.legend()
plt.grid()

# Tampilkan plot di Streamlit
st.pyplot(plt)


plt.figure(figsize=(10, 6))
sns.boxplot(x='holiday', y='cnt', data=day_df, palette='Set2')

plt.title('Perbandingan Jumlah Sewa Sepeda pada Hari Libur dan Hari Kerja')
plt.xlabel('Hari (0 = Workingday, 1 = Holiday)')
plt.ylabel('Jumlah Sewa Sepeda')

# Tampilkan plot di Streamlit
st.pyplot(plt)






st.header('Wawasan Utama')
st.write("""
- Terdapat perbedaan signifikan dalam penyewaan sepeda antara hari libur dan hari kerja, dengan hari kerja menunjukkan rata-rata penyewaan yang lebih tinggi.
- Akhir pekan juga menunjukkan tren penyewaan yang lebih tinggi dibandingkan dengan hari kerja biasa.
- Penyewaan sepeda mencapai puncaknya antara pukul 17:00 dan 19:00, menunjukkan penggunaan yang lebih tinggi selama jam pulang kerja.
""")

# Elemen interaktif
st.header('Jelajahi Data')
if st.checkbox('Tampilkan data mentah'):
    st.subheader('Data mentah')
    st.write(day_df)

st.subheader('Penyewaan Harian')
selected_date = st.date_input('Pilih tanggal', min_value=pd.to_datetime(day_df['dteday']).min(),
                              max_value=pd.to_datetime(day_df['dteday']).max())
filtered_data = day_df[pd.to_datetime(day_df['dteday']).dt.date == selected_date]
if not filtered_data.empty:
    st.write(f"Total penyewaan pada {selected_date}: {filtered_data['cnt'].values[0]}")
else:
    st.write("Tidak ada data tersedia untuk tanggal yang dipilih.")

# Jalankan aplikasi Streamlit
if __name__ == '__main__':
    st.sidebar.info(
        'Dashboard ini menyediakan wawasan tentang pola penyewaan sepeda berdasarkan analisis yang diberikan.')