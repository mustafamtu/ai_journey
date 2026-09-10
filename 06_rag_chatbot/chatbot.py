import sqlite3
import uuid
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory

load_dotenv()

class ChatbotManager:
    def __init__(self, model_name: str = "gpt-4o-mini", db_path: str = "history.db"):
        """
        Chatbot yöneticisini başlatır.
        :param model_name: Kullanıcılacak OPENAI modeli (Varsayılan: gpt-4o-mini)
        :param db_path: Geçmişin tutulacağı veritabanı yolu
        """
        self.model_name = model_name
        self.db_file_path = db_path
        self.connection_str = f"sqlite:///{db_path}"
        self.LLM = ChatOpenAI(model=self.model_name)

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

    def _create_chain(self):
        """
        Prompt ve LLM'i birleştiren hafızalı zinciri oluşturur.
        """

        prompt = ChatPromptTemplate.from_messages([
            ("system", "Sen yardımsever bir asistansın."),
            MessagesPlaceholder(variable_name="gecmis"),
            ("human", "{soru}")
        ])

        chain = prompt | self.LLM

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

            return response.content
        except Exception as e:
            return f"Bir hata oluştu: {str(e)}"
        
    def chat_stream(self, session_id: str, query: str):
        config = {"configurable": {"session_id": session_id}}

        try:
            for chunk in self.conversation_chain.stream(
                {"soru": query},
                config=config
            ):
                yield chunk.content
        except Exception as e:
            return f"Bir hata oluştu: {str(e)}"

        
if __name__ == "__main__":
    bot = ChatbotManager()

    user = "sadikturan"

    sessions = bot.list_sessions(user)

    if not sessions:
        session_id = bot.create_session(user, title="Python Dersleri Hakkında")
        print(session_id)
    else:
        print(f"Bulunan sohbet sayısı: {len(sessions)}")
        session_id = sessions[0]['session_id'] #en son sohbet
        print(session_id)