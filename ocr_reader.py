# OCR ile imageler okuyup veriler ayrı bir txt dosyasına kaydediyoruz 

import pytesseract  # tesseract 
from PIL import Image  # görseli açma kütüphanesi
import os

def read_and_save_all(input_dir="images", output_dir="output/ocr_text"):
    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(input_dir):  # klasördeki her şeyi listeler png ile biten 
        if file.endswith(".png"):
            img_path = os.path.join(input_dir, file)
            print(f" OCR : {file} işleniyor...")

            text = pytesseract.image_to_string(Image.open(img_path))

            # çıktıyı txt dosyasına kaydetme 
            out_path = os.path.join(output_dir, file.replace(".png", "_ocr.txt"))
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(text)

    print(f"\n  OCR tamamlandı, sonuçlar '{output_dir}' içine kaydedildi.")

if __name__ == "__main__":
    read_and_save_all()
