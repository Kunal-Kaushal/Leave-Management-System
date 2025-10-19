import google.adk as adk
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

# We only need to import the top-level Orchestrator
from agents.orchestrator_agent import OrchestratorAgent

# --- Load Environment Variables ---
load_dotenv()

# --- Pydantic Models ---
class ChatRequest(BaseModel):
    message: str
    user_id: str = "adk_test_user"

# --- FastAPI App Initialization ---
app = FastAPI(
    title="ADK Leave Management System",
    description="An API for managing leave requests using a multi-agent system.",
    version="1.0.0",
)

# --- API Endpoints ---
@app.get("/")
async def root():
    return {"message": "Welcome to the ADK Leave Management System!"}

@app.post("/chat")
async def handle_chat(request: ChatRequest):
    print(f"Received message from '{request.user_id}': '{request.message}'")
    
    runner = adk.Runner()
    result = await runner.run_async(
        agent=OrchestratorAgent,
        prompt=request.message
    )
    
    final_response = result.output
    
    print(f"ADK Agent Response: {final_response}")
    return {"reply": final_response}



