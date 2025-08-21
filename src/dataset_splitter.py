'''
Elimizdeki Dataseti incelediğimizde test, train ve val adlı klasörler ve bu klasörlerde fiş resimleri bulunan png uzantılı dosyalar var.
bu kalsörlerde ayrıca png dosyalarının içeriği bulunduran aynı isimli txt uzantılı dosyalar var.
bu png leri ve txt leri ayırıp png den ocr ile okuduğumuz verilerin doğrulugunu txt dosyalarından kontrol edicez
'''

import os #klasörler içinde dosya arama ve yol birleştirme için 
import shutil #dosya kopyalama taşıma silme 

#kaggeldan indirdiğimiz dataset klasör isimler
folders=["train", "val","test"]

#klasörleri ayıklayıp kendi klasörlerimize ekleyeceğiz 
images_dir = os.path.join("separated dataset", "images")  # png dosyaları
labels_dir = os.path.join("separated dataset", "labels")  # txt dosyalarıs

#yeni klasörleri oluştur
os.makedirs(images_dir, exist_ok=True)
os.makedirs(labels_dir, exist_ok=True)

#her bir klasörü dolaş
for folder in folders:
    folder_path= os.path.join("original dataset",folder) # dataset ana klasörü original dataset
    for file_name in os.listdir(folder_path):
        src_path=os.path.join(folder_path, file_name)

         #png ile bitenleri images klasörüne kaydet 
        if file_name.endswith(".png"):
            dst_path = os.path.join(images_dir, file_name)
            shutil.copy(src_path, dst_path)#kopyala

            #txt ile bitenleri label klasörüne kaydet
        elif file_name.endswith(".txt"):
            dst_path= os.path.join(labels_dir, file_name)
            shutil.copy(src_path, dst_path)

print(" Tüm png'ler separated dataset/images/, txt'ler separated dataset/labels/ klasörüne toplandı!")
