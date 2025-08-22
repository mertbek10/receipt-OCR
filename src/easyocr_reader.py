'''
tesseract sonrası karşılaştırma için easyocr denemesi yapıyoruz
tesseracta göre çok yavaş okuduğu gpu kullanması için python 3.10.9 sürümüne ve başka bir sanal ortama geçtim
'''

# images leri OCR ile okuyup texte kaydettiğimiz dosya (EasyOCR versiyonu)
import easyocr
import cv2
import os
import torch

# GPU desteğini otomatik kontrol et
use_gpu = torch.cuda.is_available()
print(f" EasyOCR başlatılıyor... GPU kullanılacak mı? {use_gpu}")

# EasyOCR okuyucu (İngilizce + Türkçe destekli, GPU varsa aktif)
reader = easyocr.Reader(['en', 'tr'], gpu=True)

def process_all_images(input_dir="separated dataset/images", output_dir="OCR output/easyocr text"):
    os.makedirs(output_dir, exist_ok=True)

    for idx, file in enumerate(os.listdir(input_dir)):
        if file.endswith(".png"):
            img_path = os.path.join(input_dir, file)
            print(f"EasyOCR : {file} işleniyor...")

            # Görseli oku
            img = cv2.imread(img_path)

            # Eğer görsel okunamazsa atla
            if img is None:
                print(f"Hatalı görsel okunamadı: {file}")
                continue

            # Görseli her zaman 3 kanallı hale getir
            if len(img.shape) == 2:  
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
            elif img.shape[2] == 4:  
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            # EasyOCR ile OCR
            results = reader.readtext(img, detail=0)  # sadece metinleri al
            text = "\n".join(results)

            # çıktıyı txt dosyasına kaydet
            out_path = os.path.join(output_dir, file.replace(".png", "_ocr.txt"))
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(text)

    print(f"\nEasyOCR tamamlandı, sonuçlar '{output_dir}' klasörüne kaydedildi.")

if __name__ == "__main__":
    process_all_images()
