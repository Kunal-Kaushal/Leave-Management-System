from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import google.generativeai as genai
from setup_database import get_leave_balance

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY environment variable not found. Please set it in your .env file.")

class ChatRequest(BaseModel):
    message: str
    user_id : str="local_test_user"

app=FastAPI(
    title="Leave Management Agent API",
    description="An API for managing leave through a conversational agent.",
    version="1.0.0",
)

system_instruction="You are a friendly and helpful assistant for an employee leave management system. Your name is Lee." 
model=genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=system_instruction,
    tools=[get_leave_balance] 
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Leave Management Agent API!"}


@app.post("/chat")
async def handle_chat(request: ChatRequest):
    """
    This endpoint receives a message from a user, prints it,
    and sends a simple, hardcoded reply. This is where our AI logic will go.
    """
    print(f"Received message from '{request.user_id}': '{request.message}'")
    chat = model.start_chat(enable_automatic_function_calling=True)
    response =chat.send_message(request.message)
    ai_reply = response.text
    print(f"AI reply: {ai_reply}")
    

    
    return {"reply": ai_reply}