from langchain_chroma import Chroma
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

embeddings= HuggingFaceEmbeddings(   
    model="sentence-transformers/all-MiniLM-L6-v2"
)

persist_directory = "./chroma_db_veri"

vectorstore = Chroma(
    embedding_function=embeddings,
    persist_directory=persist_directory,
)

# sonuclar = vectorstore.similarity_search_with_score("soru", k=3)

retriever = vectorstore.as_retriever(search_kwargs={"k":4})
chat_model = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    temperature = 0
)


def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "Aura Sound Pro-X1 için teknik destek asistanısın. "
                "Cevap verirken doğrudan kullanıcıya hitap et, asla kendi rolünü veya kimliğini tanıtarak başlama. "
                "Yalnızca aşağıdaki bağlamı kullan:\n\n{context}"
            ),
        ),
        ("human", "{question}"),
    ]
)

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | chat_model
    | StrOutputParser()
)

sonuc = chain.invoke("Bu kulaklık hangi ülkeden geliyor")

print(sonuc)
  

# arama("Pil Ömrü ne kadar?")
# arama("pil rengi kırmızıysa durum nedir?")
