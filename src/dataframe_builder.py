'''
OCR ile okuyup çıktıları txt dosyası olarak kaydettiğimiz yerden verileri alıp ayrıştırma işlemi yapıyoruz
bu ayrıştırmayı kendi istediğimiz kolonlara göre yapıcaz
'''
import os #klasörler içinde dosya aramak yol birliştirmek için
import re #metinleri ayıklamak için kullanılan kütüphane regular experssions
import pandas as pd #dataframe oluşturmak için 

def parse_receipt_text(text):
    #OCR çıktısından istediğimiz kolonları ayıkla
    data = {
        "customer_name": None,
        "date": None,
        "time": None,
        "total": None,
        "payment_method": None,
    }

#OCR dan gelen texti satırlara ayırıyourz
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    # Customer name → ilk satır
    if lines:
     data["customer_name"] = lines[0]

    # regex çıkarımı 
    # Date (22/12/2018 veya 22-12-2018 formatı)
    match = re.search(r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", text)
    if match:
        data["date"] = match.group(1)

    # Time (08:13:39 AM / 8:13 AM / 20:13 gibi)
    match = re.search(r"(\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM)?)", text, re.IGNORECASE)
    if match:
        data["time"] = match.group(1)

    # Total (Total, Grand Total, Amount Due vs.)
    match = re.search(r"(?:Total|Grand Total|Amount Due|Balance).*?(\d+\.\d{2})", text, re.IGNORECASE)
    if match:
        data["total"] = match.group(1)

    # Payment method
    if "cash" in text.lower():
        data["payment_method"] = "Cash"
    elif "credit" in text.lower() or "visa" in text.lower() or "master" in text.lower():
        data["payment_method"] = "Credit"

     
    return data



def extract_all_receipts(input_dir="OCR output/ocr_text"):
    rows = []
    files = [f for f in os.listdir(input_dir) if f.endswith(".txt")]

    for file in files:
        with open(os.path.join(input_dir, file), "r", encoding="utf-8") as f:
            text = f.read()
        parsed = parse_receipt_text(text)
        rows.append(parsed)

    df = pd.DataFrame(rows)# DATAFRAME KAYDEDİLDİ

    '''
    tüm verileri terminale yazması hem uzun süreceği hem de karmaşık gözükeceği için 
    Sadece ilk 5 satırı terminalde göster
    '''
    print("İlk 5 fişin çıktısı:")
    print(df.head())

    # Toplam kaç fiş işlendi mesajı
    print(f"\nTüm dosyalar işlendi, toplam {len(df)} fiş işlendi.")
     
     #eksik değer kontrolu
    print(df.isnull().sum())
    

    return df


if __name__ == "__main__":
    extract_all_receipts()
