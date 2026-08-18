from google import genai
import json

my_api_key = "-"

class SentimentAnalyzer:
    def __init__(self):
        try:
            self.client = genai.Client(api_key = my_api_key)
            self.model_id = "gemini-2.5-flash"
        except Exception as e:
            print(f"Bağlantı Hatası: {e}")

    def analyze_text(self, text):
        if not text:
            return {"error:" ,"Boş Metin Gönderildi."}

        prompt = f"""
            Sen profesyönel bir duygu analizi uzmanı ve dil uzmanısın 
            Aşağıdaki metni analiz et.

            {text}

            Lütfen yanıtını SADECE (başka hiçbir açıklama olmadan) aşağıdaki JSON formatında ver:

            {
                {
                    "sentiment": "Pozitif, Negatif veya Nötr",
                    "score": "0 ile 100 arası bir puan (100 = Çok Olumlu / 0 = Çok Olumsuz)",
                    "summary": "Metnin ana fikri (Maksimum 10 kelime)",
                    "language": "Metnin Dili (tr,en,ar,de vb.)"
                }
            }
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_id, 
                contents=prompt,
                config ={
                    'response_mime_type':'application/json'
                }
                )
            clean_text = response.text.replace("```json","").replace("```","").strip()
            result = json.loads(clean_text)
            return result
        except Exception as ex:
            print(f"Hata Oluştu: {ex}")

            return {
                "sentiment": "Hata",
                "score": 0,
                "summary": "Analiz sırasında bir hata oluştu",
                "language": "Bilinmiyor",
                "error_detail": str(ex)
            }
        

if __name__ == "__main__":
    analizci = SentimentAnalyzer()

    # ornek_yorum = "Ürün harika kargo da tam zamanında geldi çok memnunum bu kötü yorum atanlar rakip firmadan herhalde."
    ornek_yorum = "Yarın kapında yazan ürün 6 günde geldi. 3.gün müşteri hizmetleri ile görşütüm herşey normal, yapacağınız şey beklemek bir sorun görünmüyor cevabını aldım ve üzerine 3 gün daha bekledim. Halbuki böyle olacağını bilseydim başka yerden alırdım. Onun dışında ürün güzel."


    sonuc = analizci.analyze_text(ornek_yorum)

    print(sonuc)