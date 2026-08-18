from google import genai

my_api_key = "-"

client = genai.Client(api_key=my_api_key)

try:
    response = client.models.generate_content(
        model = "gemini-3.7-flash",
        contents = "Bana yazılımcılarla ilgili çok kısa, tek cümlelik komik bir şaka yapar mısın?"
    )
    print(response.text)

except Exception as e:
    print("Hata Oluştu. \n")
    print(f"Hata Detayı : {e}")
