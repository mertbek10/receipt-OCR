# images leri ocr ile okuyup texte kaydettiğmiz dosya 
# görüntü daha iyi okunabilsin diye preprocessing uyguluyoruz 

import pytesseract#ocr için tesseract
import cv2 #image processing için 
import os #klasörler içinde gezinip yol oluşturma

''' 
ocr sonrası metin ayıklarken none değerler vardı 
bunları azaltmak için preprocessing yapıyoruz 
görüntünün okunaklığını arttırmak için görüntü işleme yapıcaz
 '''
#görüntü isleme
# simple mode görüntü işleme tekniğini kullandık
def preprocess_image(img_path, mode="simple", save_debug=False, debug_dir="OCR output/processed image"):
    img = cv2.imread(img_path) #görseli okuma
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #görseli griye çevir

    
    if mode == "simple":
        processed = cv2.medianBlur(gray, 3)
    else:
        processed = gray

    '''
    debug istenirse kaydet 
    imagenin işlendikten sonraki halini görmek için 1 tane imagei kaydediyoruz 
    '''
    if save_debug:
        os.makedirs(debug_dir, exist_ok=True)
        base = os.path.basename(img_path)
        debug_path = os.path.join(debug_dir, base.replace(".png", "_processed.png"))
        cv2.imwrite(debug_path, processed)
        print(f"precessed image=CR output tesseract_processed klasörüne kaydedildi: {debug_path}")

    return processed

# görüntüleri al ve tesseract ile okuduktan sonra text dosylarına yaz 
def process_all_images(input_dir="separated dataset/images", output_dir="OCR output/ocr text"):
    os.makedirs(output_dir, exist_ok=True)

    for idx, file in enumerate(os.listdir(input_dir)):
        if file.endswith(".png"):
            img_path = os.path.join(input_dir, file)
            print(f"OCR : {file} işleniyor...")

            # sadece ilk görsel için debug kaydı
            processed_img = preprocess_image(img_path, mode="simple", save_debug=(idx == 0))

            # OCR 
            config = "--psm 6"
            text = pytesseract.image_to_string(processed_img, lang="eng", config=config)

            # çıktıyı txt dosyasına kaydet
            out_path = os.path.join(output_dir, file.replace(".png", "_ocr.txt"))
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(text)

    print(f"\nOCR tamamlandı, sonuçlar '{output_dir}' klasörüne kaydedildi.")

if __name__ == "__main__":
    process_all_images()
