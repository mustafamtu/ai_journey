from analyzer import SentimentAnalyzer
import os

analizci = SentimentAnalyzer()
dosya_yolu = "yorumlar.txt"
rapor_yolu = "analiz_raporu.txt"

print("Analiz Sistemi Başlatılıyor...")

sonuclar = []

if os.path.exists(dosya_yolu):
    with open(dosya_yolu,"r",encoding="utf-8") as f:
        satirlar = f.readlines()
    print(f"Toplam {len(satirlar)} adet yorum bulundu. İşleniyor...")

    for satir in satirlar:
        yorum = satir.strip()
        if not yorum: continue
        print(f"İnceleniyor: {yorum}")
        

        analiz_sonucu = analizci.analyze_text(yorum)

        analiz_sonucu["original_text"] = yorum

        sonuclar.append(analiz_sonucu)

    print("\n Tüm Yorumlar Analiz Edildi. Rapor Hazırlanıyor...")

    toplam_yorum = len(sonuclar)
    pozitif_sayisi = sum(1 for x in sonuclar if x['sentiment'] == 'Pozitif')                      
    negatif_sayisi = sum(1 for x in sonuclar if x['sentiment'] == 'Negatif')
    notr_sayisi = toplam_yorum - (pozitif_sayisi + negatif_sayisi)

    en_mutlu = max(sonuclar, key = lambda x: int(x['score']))   
    en_kizgin = min(sonuclar, key = lambda x: int(x['score']))   

    # Raporu dosyaya yaz

    rapor_icerigi = f"""
        --- YORUM/DUYGU ANALİZ RAPORU ---

        Genel Durum
        ------------------
        Toplam yorum : {toplam_yorum}
        Pozitif      : {pozitif_sayisi}
        Negatif      : {negatif_sayisi}
        Nötr         : {notr_sayisi}

        En Mutlu Müşteri {en_mutlu['score']} Puan
       
        En Kızgın Müşteri {en_kizgin['score']} Puan

    """ 
    with open(rapor_yolu,"w",encoding='utf-8') as f:
        f.write(rapor_icerigi)

    print(f"Rapor Başarıyla Oluşturuldu.")
else:
    print("Dosya Yolu Bulunamadı")



