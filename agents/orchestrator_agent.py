import os
from google.adk.agents import LlmAgent

from .specialist_agents import (
    BalanceCheckAgent,
    EmailDraftAgent,
    EmailSendAgent
)

# --- The Orchestrator (Manager) Agent ---
OrchestratorAgent = LlmAgent(
    name="OrchestratorAgent",
    model="gemini-2.5-flash",
    
    sub_agents=[
        BalanceCheckAgent,
        EmailDraftAgent,
        EmailSendAgent
    ],
    
    instruction=(
        "You are the central orchestrator for an employee leave management system. "
        "Your job is to understand the user's intent and delegate the task to the correct specialist sub-agent. "
        
        "--- Routing Rules ---"
        "1. If the user wants to **check their leave balance**, delegate to the `BalanceCheckAgent`. "
        "2. If the user wants to **draft a new leave email**, delegate to the `EmailDraftAgent`. "
        "3. If the user wants to **send an email**, delegate to the `EmailSendAgent`. "
        
        "--- Editing Rule ---"
        "4. If the user wants to **edit an email** that was just drafted, you must handle this yourself. "
        "Take the email from the conversation history and the user's edit request (e.g., 'make it more casual') and generate the new, edited email draft as your response."
    )
)

root_agent=OrchestratorAgent





