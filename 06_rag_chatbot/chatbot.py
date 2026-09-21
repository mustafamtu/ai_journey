import sqlite3
import uuid
from click import prompt
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_chroma import Chroma
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import RunnablePassthrough, RunnableBranch


load_dotenv()

class ChatbotManager:
    def __init__(self, model_name: str = "gemini-2.5-flash", db_path: str = "history.db"):
        """
        Chatbot yöneticisini başlatır.
        :param model_name: Kullanıcılacak GEMINI modeli (Varsayılan: gemini-2.5-flash)
        :param db_path: Geçmişin tutulacağı veritabanı yolu
        """
        self.model_name = model_name
        self.db_file_path = db_path
        self.connection_str = f"sqlite:///{db_path}"
        self.LLM = GoogleGenerativeAI(model=self.model_name)
        self.embedding_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2")

        persist_directory = "./chroma_db_veri"
        self.vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embedding_model
        )

        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k":3})

        self._init_session_db()

        # zinciri kur
        self.conversation_chain = self._create_chain()   
 
    def _init_session_db(self):
        """
        Sohbet başlıklarını ve sahiplerini tutan tabloyu oluştur.
        Lanchain mesajları 'message_store' tablosunda tutar, biz ise 'chat_sessions' tablosunda oturum listesini tutacağız.
        """

        conn = sqlite3.connect(self.db_file_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_sessions(
                session_id TEXT PRIMARY KEY,
                user_id TEXT,
                title TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
        conn.close()

    def _get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        """
        Belirtilen session_id için SQL geçmişini getirir.
        """
        return SQLChatMessageHistory(
            session_id=session_id,
            connection=self.connection_str
        )

    def _format_docs(self, docs):
        return "\n\n".join([d.page_content for d in docs])

    def _get_router_chain(self):
        router_system = """
        Sen bir sınıflandırma asistanısın. Sana gelen soruyu analiz et.

        KURALLAR:
        1- Eğer soru KVKK, Kanun, Cezalar, Veriler, Rıza gibi teknik ve hukuki konularla ilgiliyse => "RAG" yaz.
        2- Eğer soru genel sohbet, selamlaşma, kişisel sorular içeriyorsa => "CHAT" yaz.

        SADECE tek bir kelime ile cevap ver ("RAG" veya "CHAT"). Başka hiçbir şey yazma.
        """

        router_prompt = ChatPromptTemplate.from_messages([
            ("system", router_system),
            ("human", "{soru}")
        ])

        return router_prompt | self.LLM | StrOutputParser()
    
    def _get_chat_chain(self):
          prompt = ChatPromptTemplate.from_messages([
            ("system", "Sen nazik bir asistansın. Kullanıcı ile sohbet et."),
            MessagesPlaceholder(variable_name="gecmis"),
            ("human", "{soru}")
            ])
          return prompt | self.LLM | StrOutputParser()
        

    def _get_rag_chain(self):
        rephrase_system = """
        
        Sohbet geçmişini ve son kullanıcı sorusunu dikkate al
        Eğer kullanıcı "bunu", "şunu", "o süreyi", "bu durumda" gibi önceki sohbete atıfta bulunan ifadeler kullanıyor ise 
        soruyu tek başına anlaşılır, tam bir arama cümlesine dönüştür.
        
        Eğer soru zaten netse 
        Örneğin: "KVKK Nedir?"
        soruyu aynen bırak ASLA cevap verme, sadece düzeltilmiş soruyu çıktı olarak ver.
        """
        
        
        # Aşama 2: Cevap üretme
        system_prompt = """
        Sen uzman bir KVKK asistanısın.
        Kullanıcının sorusunu cevaplamak için 
        öncelikle aşağıdaki BAĞLAM (Context) bilgisini kullan
        Eğer bağlamda cevap yoksa üzülerek dökümanda bulamadığını söyle ve asla uydurma cevap verme.
        
        Bağlam:
        {context}
        """
        
        rephrase_prompt = ChatPromptTemplate.from_messages([
                    ("system", rephrase_system),
                    MessagesPlaceholder(variable_name="gecmis"),
                    ("human", "{soru}")
                ])
        rephrase_chain = rephrase_prompt | self.LLM | StrOutputParser()
    
                
        
        def inspect_query(query):
                    print("Retriever'a gönderilen sorgu:", query)
                    return query
                
        return (
        RunnablePassthrough.assign(
            search_query = rephrase_chain
        )
        |
        RunnablePassthrough.assign(
        context = itemgetter("search_query") | RunnableLambda(inspect_query) | self.retriever | self._format_docs,
        )
        | prompt
        | self.LLM
        | StrOutputParser()
        )
        


    def _create_chain(self):
        """
        Router mimarisi ile kullanıcıyı gereken yapıya götüren fonksiyon
        """

        # Aşama 1: Parçaların hazırlanması  
        
        
          
        router_chain = self._get_router_chain()
        chat_chain = self._get_chat_chain()
        rag_chain = self._get_rag_chain()

        # Aşama 2: Karar Mekanizması (Dallanma/Branch)

        branch = RunnableBranch(
            (lambda x: "RAG" in x["topic"], rag_chain),
            chat_chain
        )

        # Aşama 3: Zincir montajı

        chain = RunnablePassthrough.assign(topic=router_chain) | branch
    


        
        return RunnableWithMessageHistory(
            chain,
            self._get_session_history,
            input_messages_key="soru",
            history_messages_key="gecmis"
        )
    
    def create_session(self, user_id: str, title: str ="Yeni Sohbet") ->  str:
        """
        Belirli bir kullanıcı için yeni sohbet oturumu oluşturur. Benzersiz bir session_id döner.
        """
        session_id = str(uuid.uuid4()) #örn: 550e85 89890

        conn = sqlite3.connect(self.db_file_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chat_sessions (session_id, user_id, title) VALUES (?,?,?)", (session_id, user_id, title)
        )
        conn.commit()
        conn.close()

        return session_id
    
    def list_sessions(self, user_id: str):
        """
        Kullanıcını tüm eski sohbetlerini listeler. (id, başlık, tarih)
        """
        conn = sqlite3.connect(self.db_file_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT session_id, title, created_at FROM chat_sessions WHERE user_id=? ORDER BY created_at DESC", (user_id,)
        )
        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]
    
    def update_session_title(self, session_id: str, new_title: str):
        """
        Sohbet başlığını güncelle.
        """
        conn = sqlite3.connect(self.db_file_path)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE chat_sessions SET title=? WHERE session_id=?", (new_title,session_id)
        )
        conn.commit()
        conn.close()

    def get_messages(self, session_id: str):
        """
        Bir oturumdaki mesaj geçmişini döner.
        """
        history = self._get_session_history(session_id)
        return history.messages
    
    def chat(self, session_id: str, query: str) -> str:
        """
        Bot ile sohbet için dışarıya açılan metod.
        """
        config = {"configurable": {"session_id": session_id}}

        try:
            response = self.conversation_chain.invoke(
                {"soru": query},
                config=config
            )

            return response
        except Exception as e:
            return f"Bir hata oluştu: {str(e)}"
        
    def chat_stream(self, session_id: str, query: str):
        config = {"configurable": {"session_id": session_id}}

        try:
            for chunk in self.conversation_chain.stream(
                {"soru": query},
                config=config
            ):
                yield chunk
        except Exception as e:
            return f"Bir hata oluştu: {str(e)}"

        
if __name__ == "__main__":
    bot = ChatbotManager()

    user = "mustafamutlu"

    session_id = bot.create_session(user, "Retriever Testi")
    # print(bot.chat(session_id, "Açık Rıza nedir?"))
    # print(bot.chat(session_id, "Bu dediğini bir dha açıklar mısın?"))
    print(bot.chat(session_id, "Merhaba, Nasılsın?"))
    print(bot.chat(session_id, "Açık Rıza nedir?"))
    


