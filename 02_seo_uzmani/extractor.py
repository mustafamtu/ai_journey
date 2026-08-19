import json
import os
import warnings
from dotenv import load_dotenv
from google import genai
from google.genai import types

warnings.filterwarnings("ignore", category=UserWarning)

load_dotenv()


class KeywordExtractor:

  def __init__(self):
    api_key = os.getenv("my_api_key")
    if not api_key:
      raise ValueError("API Key Bulunamadı.")

    self.client = genai.Client(api_key=api_key)
    self.model_id = "gemini-2.5-flash"

  # 1. ORTAK MOTOR: Gemini'yi çağırıp JSON çözen fonksiyon
  def _call_gemini(self, system_prompt, text, json_key):
    user_prompt = f"Metin: {text}"
    print("AI Çalışıyor...")

    try:
      response = self.client.models.generate_content(
          model=self.model_id,
          contents=user_prompt,
          config=types.GenerateContentConfig(
              system_instruction=system_prompt,
              response_mime_type="application/json",
              temperature=0.4,
          ),
      )

      raw_content = response.text
      parsed_content = json.loads(raw_content)
      return parsed_content.get(json_key, [])

    except Exception as e:
      print(f"Hata: {e}")
      return []

  # 2. GÖREV: Anahtar Kelimeleri Çıkar
  def extract_keywords(self, text):
    if not text:
      return []

    system_prompt = """
        Sen deneyimli bir SEO Uzmanısın.
        Görevin verilen metinden en önemli 5 anahtar kelimeyi bulmaktır.
        Cevabı SADECE şu JSON formatında ver:
        {"keywords": ["kelime1", "kelime2", "kelime3", "kelime4", "kelime5"]}
        """
    return self._call_gemini(system_prompt, text, "keywords")

  # 3. GÖREV: Hashtag Üret (Eksik olan buydu!)
  def extract_hashtags(self, text):
    if not text:
      return []

    system_prompt = """
        Sen yaratıcı bir sosyal medya yöneticisisin.
        Görevin verilen metinden paylaşılabilir, popüler 5 adet hashtag üretmektir.
        Her kelimenin başında '#' işareti olsun.
        Cevabı SADECE şu JSON formatında ver:
        {"hashtags": ["#tag1", "#tag2", "#tag3", "#tag4", "#tag5"]}
        """
    raw_tags = self._call_gemini(system_prompt, text, "hashtags")

    formatted_tags = [self._format_tag(tag) for tag in raw_tags]

    return formatted_tags


  def _format_tag(self, tag):
    clean_tag = tag.replace(" ", "").lower()

    if not clean_tag.startswith("#"):
      clean_tag = f"#{clean_tag}"

    return clean_tag
    
def main():
  extractor = KeywordExtractor()

  test_metni = """
    Python, günümüzün en popüler programlama dillerinden biridir.
    Özellikle Yapay Zeka, Veri Bilimi ve Web Geliştirme alanlarında sıkça kullanılır.
    Django ve FastAPI gibi kütüphaneler sayesinde hızlıca API geliştirebilirsiniz.
    """

  print(f"Analiz edilen metin:\n{test_metni}")
  print("-" * 40)

  # 1. Anahtar kelimeler
  keywords = extractor.extract_keywords(test_metni)
  print("\n--- Çıkarılan Anahtar Kelimeler ---")
  for i, kelime in enumerate(keywords, 1):
    print(f"{i}. {kelime}")

  print("-" * 40)

  # 2. Hashtag'ler
  hashtags = extractor.extract_hashtags(test_metni)
  print("\n--- Çıkarılan Hashtag'ler ---")
  for i, tag in enumerate(hashtags, 1):
    print(f"{i}. {tag}")


if __name__ == "__main__":
  main()