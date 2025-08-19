'''
Elimizdeki Dataseti incelediğimizde test train ve val adlı klasörler ve bu klasörlerde fiş resimleri bulunan png dosyaları var.
bu kalsörlerde ayrıca png dosyalarının içeriği bulunduran aynı isimli txt dosyaları var.
bu png leri ve txt leri ayırıp png den ocr ile okuduğumuz verilerin doğrulugunu txt dosyalarından kontrol edicez
'''

import os
import shutil

#kaggeldan indirdiğimiz dataset klasör isimler
folders=["train", "val","test"]

#klasörleri ayıklayıp kendi klasörlerimize ekleyeceğiz 
images_dir= "images"#png dosyaları 
labels_dir="labels"#txt dosyaları 

#yeni klasörleri oluştur
os.makedirs(images_dir, exist_ok=True)
os.makedirs(labels_dir, exist_ok=True)

#her bir klasörü dolaş
for folder in folders:
    folder_path= os.path.join("original dataset",folder) # dataset ana klasörü findit2
    for file_name in os.listdir(folder_path):
        src_path=os.path.join(folder_path, file_name)

        if file_name.endswith(".png"):
            dst_path = os.path.join(images_dir, file_name)
            shutil.copy(src_path, dst_path)#kopyala
        elif file_name.endswith(".txt"):
            dst_path= os.path.join(labels_dir, file_name)
            shutil.copy(src_path, dst_path)

print(" Tüm png'ler images/, txt'ler labels/ klasörüne toplandı!")
