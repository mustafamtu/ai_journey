from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

dosya_adi = "kullanim_kilavuzu.pdf"

loader = PyPDFLoader(dosya_adi)
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=30,
)

parcalar = splitter.split_documents(docs)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004"
)

persist_directory = "./chroma_db_veri"
print("Vektör Veritabanı oluşturuluyor...")

vectorstore = Chroma.from_documents(
    documents=parcalar,
    embedding=embeddings,
    persist_directory=persist_directory,
)

print(f"Başarılı! Veriler {persist_directory} klasörüne kaydedildi.")