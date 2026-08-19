from google import genai
from dotenv import load_dotenv
import warnings
import os

warnings.filterwarnings("ignore", category=UserWarning)

load_dotenv()

api_key = os.getenv("my_api_key")

if not api_key:
    print("Hata: API Key bulunamadı.")
else:
    print(f"Anahtar Başarıyla Yüklendi. ({api_key[:5]}...***)")

    client = genai.Client(api_key=api_key)

    print("Google AI Studio Hazırlanıyor...")

    try:
        response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = (
                "Yapay zeka mühendislerine motive edici tek bir cümle söyler misin?"
            )
        )

        print("-" * 40)
        print(f"AI Cevabı:\n {response.text}")
        print("-" * 40)
    except Exception as e:
        print(f"Bağlantı Hatası: {e}")
        
