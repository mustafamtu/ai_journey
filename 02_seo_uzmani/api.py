# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from extractor import KeywordExtractor
# from pydantic import BaseModel
# import uvicorn

# app = FastAPI(
#     title = "API Content Analyzer API",
#     description= "Metin Analizi, SEO kelimeleri ve hashtag üretimi için servis",
#     version="1.0.0"
# )

# app.add_middleware(
#     CORSMiddleware, 
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# try:
#     extractor_service = KeywordExtractor()
#     print("AI Servisi başarıyla yüklendi")
# except Exception as e:
#     print(f"Hata Oluştu: {e}")

# class AnalyzerRequest(BaseModel):
#     text: str

# @app.get("/")
# def home():
#     return {"message": "API Çalışıyor. Dökümantasyon için /docs adresine gidin"}

# @app.post("/api/hashtags")
# def get_hashtags(request: AnalyzerRequest):
#     return {"hashtags": extractor_service.extract_hashtags(request.text)}

# @app.post("/api/keywords")
# def get_keywords(request: AnalyzerRequest):
#     return {"keywords": extractor_service.extract_keywords(request.text)}

