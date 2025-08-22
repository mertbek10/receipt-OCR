import pandas as pd
import matplotlib.pyplot as plt
import calendar

# CSV dosyasını oku
df = pd.read_csv("dataframe.csv")

# Eksik (NaN) değerleri at
df = df.dropna(subset=["date", "total"])

# Tarihi datetime formatına çevir
df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)

# Total sütununu numerik hale getir
df["total"] = pd.to_numeric(df["total"], errors="coerce")

# Ay kolonunu ekle
df["month"] = df["date"].dt.month

# Aylara göre harcamaları grupla
monthly_expenses = df.groupby("month")["total"].sum()
monthly_expenses.index = monthly_expenses.index.astype(int).map(lambda x: calendar.month_name[x])

# En çok harcama yapılan ayı bul
max_month = monthly_expenses.idxmax()
max_value = monthly_expenses.max()

print(f"En çok harcama yapılan ay: {max_month} → Toplam {max_value:.2f}")


# === Grafik 1: Aylara Göre Harcama (bar chart) ===
plt.figure(figsize=(12,6))
bars = monthly_expenses.plot(kind="bar", color="skyblue", edgecolor="black")

plt.title("Aylara Göre Toplam Harcama")
plt.xlabel("Ay")
plt.ylabel("Toplam Harcama")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)

for i, v in enumerate(monthly_expenses):
    plt.text(i, v + (v*0.01), f"{v:.2f}", ha="center", va="bottom", fontsize=9, fontweight="bold")

bars.patches[list(monthly_expenses.index).index(max_month)].set_color("orange")

plt.tight_layout()
plt.show()


# === Grafik 2: Ödeme Yöntemi Dağılımı (pie chart) ===
payment_counts = df["payment_method"].dropna().value_counts()

if not payment_counts.empty:
    plt.figure(figsize=(8,8))
    plt.pie(
        payment_counts,
        labels=payment_counts.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=["gold", "lightgreen"]
    )
    plt.title("Ödeme Yöntemi Dağılımı (Cash vs Credit)")
    plt.show()
else:
    print(" Ödeme yöntemi verisi bulunamadı!")



   
from datetime import datetime

# CSV oku
df = pd.read_csv("dataframe.csv")
df = df.dropna(subset=["time"])  # boş saatleri at

def normalize_time(t):
    if pd.isna(t):
        return None
    t = str(t).strip()
    t = t.replace(".", ":").replace(" ", "")

    # AM/PM formatı
    for fmt in ["%I:%M%p", "%I:%M:%S%p"]:
        try:
            return datetime.strptime(t.upper(), fmt).time()
        except:
            continue

    # 24 saat formatı
    for fmt in ["%H:%M", "%H:%M:%S"]:
        try:
            return datetime.strptime(t, fmt).time()
        except:
            continue
    return None

df["norm_time"] = df["time"].apply(normalize_time)

def time_to_period(t):
    if t is None:
        return None
    hour = t.hour
    if 8 <= hour < 12:
        return "08-12"
    elif 12 <= hour < 20:
        return "12-20"
    elif 20 <= hour < 24:
        return "20-24"
    else:
        return "00-08"

df["time_period"] = df["norm_time"].apply(time_to_period)

# Fiş sayısını hesapla
period_counts = df["time_period"].value_counts().reindex(["08-12","12-20","20-24","00-08"])

# === Pasta Grafiği ===
plt.figure(figsize=(7,7))
plt.pie(
    period_counts,
    labels=period_counts.index,
    autopct="%1.1f%%",
    startangle=90,
    colors=["skyblue","lightgreen","gold","salmon"]
)
plt.title("Hangi Saat Diliminde Daha Çok Market Gidilmiş?")
plt.show()

