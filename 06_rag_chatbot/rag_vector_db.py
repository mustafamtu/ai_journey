import time
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

dosya_adi = "kvkk.pdf"

loader = PyPDFLoader(dosya_adi)
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=30,
)

parcalar = splitter.split_documents(docs)
print(f"Toplam {len(parcalar)} parça oluşturuldu.")

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-2"
)

persist_directory = "./chroma_db_veri"
print("Vektör Veritabanı hazırlanıyor...")

vectorstore = Chroma(
    persist_directory=persist_directory,
    embedding_function=embeddings
)

batch_size = 20
i = 0
while i < len(parcalar):
    batch = parcalar[i:i + batch_size]
    try:
        vectorstore.add_documents(documents=batch)
        print(f"{min(i + batch_size, len(parcalar))}/{len(parcalar)} parça yüklendi...")
        i += batch_size
        time.sleep(1) 
    except Exception as e:
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            print("Dakikalık 100 limitine çarpıldı. 30 saniye bekleniyor...")
            time.sleep(30) 
        else:
            raise e

print(f"Tebrikler! Tüm veriler {persist_directory} klasörüne eksiksiz kaydedildi.")