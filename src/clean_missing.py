# Dataframemimizdeki eksik değrleri temizleme-doldurma işlemini yapıcaz 

import numpy as np
import random
from dataframe_builder import extract_all_receipts #oluşturduğumuz dataframe erişmek için

#dataframe_builder.py dosyasından fonksiyona erişim saylayarak dataframe ulaşıyoruz
df=extract_all_receipts()


#eksik olan isimleri örnek aynı isimle doldur(maverik)
df["customer_name"] = df["customer_name"].fillna("maverick")

'''
time için eksik değerleri 3 aralıkta eşit olacak şekilde doldurulucak
ilerde son dataframe şeklini excel dosyasına bu 3 aralıktaki harcamalar olacak şekilde kategorize edilecek
'''
time_ranges ={ 
    "08-12": (8, 12),
    "12-20": (12, 20),
    "20-24": (20, 24),
}


def random_time_in_range(start_hour, end_hour):
    hour = random.randint(start_hour, end_hour-1)
    minute = random.randint(0, 59)
    return f"{hour:02d}:{minute:02d}"

missing_time= df["time"].isna().sum()
if missing_time > 0:
    slots = list(time_ranges.keys())
    fill_slots= np.resize(slots, missing_time)
    missing_idx =df[df["time"].isna()].index

    for idx, slot in zip(missing_idx, fill_slots):
        start, end = time_ranges[slot]
        df.loc[idx, "time"] = random_time_in_range(start, end)



#ödeme yöntemi için eksik değerleri eşit olacak şekilde card ve cash diye doldurucaz
missing_pay= df["payment_method"].isna().sum()
if missing_pay > 0:
    methods= ["card", "cash"]
    fill_methods = np.resize(methods, missing_pay)
    missing_idx = df[df["payment_method"].isna()].index
    for idx, method in zip(missing_idx, fill_methods):
        df.loc[idx, "payment_method"] = method



#tarih için eksik satırları düşür
df = df.dropna(subset=["date"])

#ödenen miktar içn eksik satırları düşür
df =df.dropna(subset=["total"])

#indexleri resetle
df = df.reset_index(drop=True)


if __name__ == "__main__":
    print("Eksik değerler dolduruldu / temizlendi")
    print(df.head())
    print(df.isnull().sum())
    



