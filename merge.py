import os
import pandas as pd
import csv


# membuat file csv sumber
import pandas as pd
columns = ['ACTIVITY_TIME', 'BATTERY', 'BLOOD_DIASTOLIC', 'BLOOD_SYSTOLIC',
           'CALORIES', 'DISTANCE', 'HEART_RATE', 'HRV', 'SLEEP',
           'SPO2', 'STEP', 'STRESS', 'TEMPERATURE', 'time', 'TANGGAL','JAM','NAMA_FILE',
           'KODE_DEVICE', 'KODE_DB', 'KATEGORI_WAKTU', 'SHIFT_PEGAWAI']

# Membuat DataFrame kosong berdasarkan nama kolom yang ditentukan
df_sumber = pd.DataFrame(columns=columns)
df_sumber.to_csv("../sumber.csv",index=False)


#mengabungkan file -  file csv pada setiap folder
df_sumber = pd.read_csv("../sumber.csv")
kolom = ['dummy_kolom']
baris = ['e']
folder_baru = "../TTL/Recap-2023-08-10_940"
#membuka setiap file pada folder
for filename in os.listdir(folder_baru):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_baru, filename)
        with open(file_path) as f:
                first_line = f.readline().strip()
                if not first_line:
                    # Menambahkan baris dummy untuk file csv tidak ada data apapun
                    with open(file_path, 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(kolom)  # Menulis kolom
                        writer.writerows(baris)  # Menulis baris
                     
        df2 = pd.read_csv(file_path)
        #membuat kolom nama, kode device, kode database
        filename = filename.split(" - ")
        df2['NAMA_FILE'] = (filename[2])
        df2['KODE_DEVICE'] = (filename[1])
        df2['KODE_DB'] = (filename[0])

        #membuat kategori shift sesuai waktu 
        if "time" in df2.columns.tolist():
            df2['time'] = pd.to_datetime(df2['time'],format='%Y-%m-%d %H:%M')
            def kategori_waktu(waktu):
                if waktu.hour < 6:
                    return 'shift 1'
                elif waktu.hour < 12:
                    return 'shift 2'
                elif waktu.hour < 18:
                    return 'shift 3'
                else:
                    return 'shift 4'
            df2['KATEGORI_WAKTU'] = df2['time'].apply(kategori_waktu)

            # Menghitung jumlah kategori shift yang paling sering muncul dari seluruh tabel
            kategori_terbanyak = df2['KATEGORI_WAKTU'].value_counts().idxmax()

            # Membuat kolom baru 'Kategori Terbanyak' dan mengisikan nilai kategori terbanyak ke setiap baris
            df2['SHIFT_PEGAWAI'] = kategori_terbanyak

            #membagi tanggal dan jam menjadi kolom tersendiri
            df2['time'] = pd.to_datetime(df2['time'])
            df2["TANGGAL"] = df2['time'].dt.date
            df2["JAM"] = df2['time'].dt.time
            #mengurutkan data berdasarkan waktu
            df2 = df2.sort_values(by='time')
        #menggabungkan setiap file csv kedalam satu file csv sumber
        df_sumber = pd.concat([df_sumber, df2], ignore_index=True)
             
        
        #menyimpan file csv kedalam file
        df_sumber.to_csv("../TTL/Recap-2023-08-10_940.csv", index=False)

   
