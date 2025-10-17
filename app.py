from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import google.generativeai as genai
from setup_database import get_leave_balance
from email_utils import draft_leave_email, send_email

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
chat_sessions = {}

system_instruction = (
    "You are Lee, a friendly and helpful AI assistant for the employee leave management system."
    "Your capabilities are: checking an employee's leave balance and drafting a formal leave request email."
    "If a user does not provide all the necessary details to use a tool (like dates or a reason for leave), you must ask clarifying questions to get the missing information."
    "After a tool is successfully used, your final response to the user MUST be only the direct output from that tool (e.g., the leave balance number or the full drafted email text). Do not add extra conversational text or summaries around the tool's output."
)
model=genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=system_instruction,
    tools=[get_leave_balance,draft_leave_email,send_email]

)

@app.get("/")
async def root():
    return {"message": "Welcome to the Leave Management Agent API!"}


@app.get("/")
async def root():
    return {"message": "Welcome to the Leave Management AI Agent API!"}


@app.post("/chat")
async def handle_chat(request: ChatRequest):
    """
    This endpoint now maintains a chat history for each user_id.
    """
    print(f"Received message from '{request.user_id}': '{request.message}'")
    
    user_id = request.user_id
    
    # Check if a chat session already exists for this user
    if user_id not in chat_sessions:
        # If not, start a new chat and store it
        print(f"Starting new chat session for user: {user_id}")
        chat_sessions[user_id] = model.start_chat(enable_automatic_function_calling=True)
    
    # Get the user's existing chat session
    chat = chat_sessions[user_id]
    
    # Send the message and get the response
    response = chat.send_message(request.message)
    ai_reply = response.text
    print(f"AI Reply: {ai_reply}")
    
    return {"reply": ai_reply}