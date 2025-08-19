# extractor.py
import os #klasörler içinde dosya aramak yol birliştirmek için
import re
import pandas as pd #dataframe oluşturmak için 

def parse_receipt_text(text):
    #OCR çıktısından istediğimiz kolonları ayıkla
    data = {
        "customer_name": None,
        "document_no": None,
        "store_name": None,
        "store_address": None,
        "date": None,
        "time": None,
        "items": None,
        "total": None,
        "payment_method": None,
    }

#OCR dan gelen texti satırlara ayırıyourz
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    # Customer name → ilk satır
    if lines:
     data["customer_name"] = lines[0]

# Document no
    match = re.search(r"(?:Document|Doc|Bill|Invoice|Receipt)\s*(?:No\.?|#)?:?\s*([A-Z0-9\-]+)", text, re.IGNORECASE)
    if match:
     data["document_no"] = match.group(1)



    # Store name → 2. satır
    if len(lines) > 1:
        data["store_name"] = lines[1]

    # Store address → 2–6 arası satırlarda adres yakala
    addr = []
    for line in lines[2:8]:
        if re.search(r"\d{5}", line) or "JALAN" in line.upper() or "ROAD" in line.upper():
            addr.append(line)
    if addr:
        data["store_address"] = " ".join(addr)

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

       # Items → fiyat geçen satırları al (ama Total satırlarını değil)
    items = []
    for line in lines:
        if re.search(r"\d+\.\d{2}", line) and not re.search(r"(Total|Grand Total|Amount Due)", line, re.IGNORECASE):
            items.append(line)
    if items:
        data["items"] = "; ".join(items)

    return data



def extract_all_receipts(input_dir="output/ocr_text"):
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
    Sadece ilk 5’i terminalde göster
    '''
    print("İlk 5 fişin çıktısı:")
    print(df.head())

    # Toplam kaç fiş işlendi mesajı
    print(f"\nTüm dosyalar işlendi, toplam {len(df)} fiş işlendi.")

    return df


if __name__ == "__main__":
    extract_all_receipts()
