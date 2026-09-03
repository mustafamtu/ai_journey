from langchain_chroma import Chroma
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

embeddings= HuggingFaceEmbeddings(   
    model="sentence-transformers/all-MiniLM-L6-v2"
)

persist_directory = "./chroma_db_veri"

vectorstore = Chroma(
    embedding_function=embeddings,
    persist_directory=persist_directory,
)

sonuclar = vectorstore.get(include=["embeddings","documents","metadatas"])

toplam_sayi = len(sonuclar["ids"])
print(f"Veritabanında toplam {toplam_sayi} parça kayıtlı. \n")

ilk_metin = sonuclar["documents"][0]
ilk_vector = sonuclar["embeddings"][0]

print(f"Metin: {ilk_metin}")
print("*" * 50)

print(f"Vektör Boyutu: {len(ilk_vector)}")
print("*" * 50)

print("Vektörün Kordinatı: ")
print(ilk_vector[:100])

