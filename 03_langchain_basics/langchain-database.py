from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory

load_dotenv()

LLM = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

prompt = ChatPromptTemplate.from_messages([
    ("system", "Sen yardımsever bir asistansın"),
    MessagesPlaceholder(variable_name="geçmiş"),
    ("human", "{soru}")
])

chain = prompt | LLM 



def get_session_history(session_id: str) -> BaseChatMessageHistory:
    return SQLChatMessageHistory(
        session_id=session_id,
        connection="sqlite:///history.db",
    )

chain_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="soru",
    history_messages_key="geçmiş",
)
    
config = {"configurable": {"session_id": "mustafamtu"}}

response2 = chain_memory.invoke(
    {"soru": "Benim adım ne, ve ben ne öğreniyorum?"},
    config=config
)

print(f"response 2 : {response2.content}")
print("-" * 30)


