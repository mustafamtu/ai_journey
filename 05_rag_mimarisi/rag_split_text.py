from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

dosya_adi = "kullanim_kilavuzu.txt"

loader = TextLoader(dosya_adi, encoding="utf-8")
docs = loader.load()
print(f"Veri Yüklendi. Karakter sayısı: {len(docs[0].page_content)}")
print(docs[0].page_content)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
)

parcalar = splitter.split_documents(docs)

# print(parcalar)

for i, parca in enumerate(parcalar):
    content = parca.page_content.replace("\n"," ")
    print(f"Parça: {i+1}  Karakter Sayısı: ({len(content)}): {content}") 