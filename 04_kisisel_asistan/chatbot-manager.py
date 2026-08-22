from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory

print("")
load_dotenv()

class ChatbotManager:
    def __init__(self, model_name: str = "gemini-2.5-flash", db_path: str = "sqlite:///history.db"):
        """
        Chatbot Yöneticisini Başlatır.

        :param self: Description
        :type model_name: Kullanılacak GEMINI Modeli (Varsayılan: gemini-2.5-flash)
        :param db_path: Geçmişin tutulacağı veritabanı yolu
        """

        self.model_name = model_name
        self.db_path = db_path
        self.LLM = ChatGoogleGenerativeAI(model=self.model_name)
        self.conversation_chain = self._create_chain()


    def get_session_history(self,session_id: str) -> BaseChatMessageHistory:
        """
        Belirtilen session_id için SQL Geçmişini getirir.
        """
                
        return SQLChatMessageHistory(
            session_id=session_id,
            connection=self.db_path
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

    session_id = "mustafamtu"

    cevap = bot.chat(session_id, "benim adım ne ve ben ne öğreniyorum.")

    print(f"Cevap: {cevap}")