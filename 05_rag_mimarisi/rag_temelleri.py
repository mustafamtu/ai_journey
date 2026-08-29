from langchain_community .document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

dosya_adi = "kullanim_kilavuzu.pdf"

loader = PyPDFLoader(dosya_adi)
docs = loader.load()

print(docs)

# print(f"Veri yüklendi. Karakter sayısı: {len(docs[0].page_content)}")
# print(docs[0].page_content)

spliter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)



parcalar = spliter.split_documents (docs)

# print(parcalar)

for i, parca in enumerate(parcalar):
    content = parca.page_content.replace("\n"," ")
    print(f"Parca: {i+1} Karakter sayısı: ({len(content)}): {content}")