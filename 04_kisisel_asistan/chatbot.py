from dotenv import load_dotenv
import sqlite3
import uuid
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory

print("")
load_dotenv()

class ChatbotManager:
    def __init__(self, model_name: str = "gemini-2.5-flash", db_path: str = "history.db"):
        """
        Chatbot Yöneticisini Başlatır.

        :param self: Description
        :type model_name: Kullanılacak GEMINI Modeli (Varsayılan: gemini-2.5-flash)
        :param db_path: Geçmişin tutulacağı veritabanı yolu
        """

        self.model_name = model_name
        self.db_file_path = db_path
        self.connection_str = f"sqlite:///{db_path}"
        self.LLM = ChatGoogleGenerativeAI(model=self.model_name)

        self._init_session_db()
        
        self.conversation_chain = self._create_chain()


    def create_session(self, user_id: str, title: str="Yeni Sohbet") -> str:
        """
        Beliri bir kullanıcı için yeni sohbet oturumu oluşturur.
        Benzersiz bir session_id döner.
        """

        session_id = str(uuid.uuid4()) #örnek: 550e85 89890

        conn = sqlite3.connect(self.db_file_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chat_sessions (session_id, user_id, title) VALUES (?,?,?)", (session_id, user_id, title)),
        conn.commit()
        conn.close()

        return session_id

    def list_sessions(self, user_id: str):
        """
        Kullanıcının tüm sohbetlerini listeler. (id, başlık, tarih)
        """

        conn = sqlite3.connect(self.db_file_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT session_id, title, created_at FROM chat_sessions WHERE user_id=? ORDER BY created_at DESC",
            (user_id,)
        )      
        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def update_session_title(self,user_id, session_id: str, new_title: str):
        """
        Sohbet Başlığını güncelle
        """
        conn = sqlite3.connect(self.db_file_path)
        cursor = conn.cursor()                
        cursor.execute(
            "UPDATE chat_sessions SET title = ? WHERE session_id=?", (new_title,session_id)
            
        )      
        conn.commit()
        conn.close()
        

    def _init_session_db(self):
        """
        Sohbet başlıklarını ve sahiplerini tutan tabloyu oluşturur.
        Langchain mesajları 'message_store' tablosunda tutar, 'chat_session' tablosunda oturum listesini
        tutacağız.
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


    def get_session_history(self,session_id: str) -> BaseChatMessageHistory:
        """
        Belirtilen session_id için SQL Geçmişini getirir.
        """
                
        return SQLChatMessageHistory(
            session_id=session_id,
            connection=self.connection_str,
        )
        
    def _create_chain(self):
        """
        Prompt ve LLM'i birleştiren hafızalı zinciri oluşturur.
        """ 
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Sen yardımsever bir asistansın"),
            MessagesPlaceholder(variable_name="geçmiş"),
            ("human", "{soru}")
        ])
        chain = prompt | self.LLM

        return RunnableWithMessageHistory(
            chain,
            self.get_session_history,
            input_messages_key="soru",
            history_messages_key="geçmiş",
        )

    def get_messages(self, session_id: str):
        """
        Bir oturumdaki mesaj geçmişini döner.
        """
        history = self._get_session_history(session_id)
        return history.messages

    def chat(self, session_id:str, query: str) -> str:
        """
        Bot ile sohbet edebilmek için dışarıya açılan metod.
        """
        config = {"configurable": {"session_id": session_id}}

        try:
            response = self.conversation_chain.invoke(
            {"soru": query},
            config=config
            )
            return response.content
        except Exception as e:
            print(f"Hata: {e}")

if __name__ == "__main__":
    bot = ChatbotManager()

    user = "mustafamtu"

    sessions = bot.list_sessions(user)

    if not sessions:
        session_id = bot.create_session(user, title= "Python Dersleri Hakkında")
        print(session_id)
    else:
        print(f"Sohbetler: {len(sessions)}")
        session_id = sessions[0]['session_id'] #en son sohbet
        print(session_id)

    print(session_id)

    # cevap = bot.chat(session_id, "benim adım ne ve ben ne öğreniyorum.")

    # print(f"Cevap: {cevap}")