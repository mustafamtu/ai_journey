from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chatbot import ChatbotManager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

class CreateSessionRequest(BaseModel):
    user_id: str
    title: str = "Yeni Sohbet"

class ChatRequest(BaseModel):
    session_id: str
    query: str

class MessageResponse(BaseModel):
    role: str
    content: str

app = FastAPI(title="Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
bot=ChatbotManager()

@app.post("/sessions/create")
def create_session(request: CreateSessionRequest):
    try:
        session_id = bot.create_session(request.user_id, request.title)
        return {"session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/sessions/{user_id}")
def list_sessions(user_id: str):
    return bot.list_sessions(user_id)
    
@app.get("/history/{session_id}")
def get_history(session_id: str):
    messages = bot.get_messages(session_id)

    result = []

    for m in messages:
        role = "user" if m.type=="human" else "assistant"
        result.append({"role": role, "content": m.content})
    return result

# @app.post("/chat")
# def chat_endpoint(request: ChatRequest):
#     cevap = bot.chat(request.session_id, request.query)
#     return {"response": cevap}

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    def iterfile():
        for chunk in bot.chat_stream(request.session_id, request.query):
            yield chunk

    return StreamingResponse(iterfile(), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)