from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

dosya_adi = "kullanim_kilavuzu.pdf"  # Dosya adındaki ı/i harfine dikkat

loader = PyPDFLoader(dosya_adi)
docs = loader.load()

print(f"Toplam Sayfa Sayısı: {len(docs)}")
if docs:
    print(f"1. Sayfa Karakter Sayısı: {len(docs[0].page_content.strip())}")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
)

parcalar = splitter.split_documents(docs)
print(f"Oluşturulan Parça Sayısı: {len(parcalar)}")

for i, parca in enumerate(parcalar):
    content = parca.page_content.replace("\n", " ")
    print(f"Parça {i+1} ({len(content)} karakter): {content}")