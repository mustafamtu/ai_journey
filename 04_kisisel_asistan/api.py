from pydantic import BaseModel
from fastapi import FastAPI,HTTPException
from chatbot import ChatbotManager

class CreateSessionRequest(BaseModel):
    user_id = str
    title: str = "Yeni Sohbet"

class ChatRequest(BaseModel):
    session_id:str
    query: str

class MessageResponse(BaseModel):
    role: str
    content: str

app = FastAPI(title="Chatbot API")
bot = ChatbotManager