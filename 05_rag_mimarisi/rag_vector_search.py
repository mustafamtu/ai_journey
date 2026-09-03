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

def arama(soru):
    print(f"Soru: {soru} aranıyor...")
    print("-" * 50)

    sonuclar = vectorstore.similarity_search_with_score(soru, k=3)

    if not sonuclar:
        print("Sonuç Bulunamadı")
        return 

    for i, (belge, puan) in enumerate(sonuclar):
        print(f"Bulunan Parça: {i+1}")
        print(f"İçerik: {belge.page_content}")
        print(f"Kaynak: {belge.metadata}")
        print(f"Benzerlik Skoru. {puan:.4f}")
        print("-" * 25)

# arama("Pil Ömrü ne kadar?")
arama("pil rengi kırmızıysa durum nedir?")
