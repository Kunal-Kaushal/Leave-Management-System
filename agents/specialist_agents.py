import os
from google.adk.agents import LlmAgent
from email_utils import draft_leave_email, send_email
from database import get_leave_balance
from pydantic import ConfigDict

MODEL_NAME = "gemini-2.5-flash"

# --- Specialist 1: The Balance Checker ---
BalanceCheckAgent = LlmAgent(
    name="BalanceCheckAgent",
    
    model=MODEL_NAME,
    tools=[get_leave_balance],
    instruction=(
        "You are a specialist. Your ONLY job is to check an employee's leave balance. "
        "When you are called, you must use the `get_leave_balance` tool."
    )
)

# --- Specialist 2: The Email Drafter ---
EmailDraftAgent = LlmAgent(
    name="EmailDraftAgent",
    
    model=MODEL_NAME,
    tools=[draft_leave_email],
    instruction=(
        "You are a specialist. Your ONLY job is to draft a professional leave request email. "
        "When you are called, you must use the `draft_leave_email` tool."
    )
)

# --- Specialist 3: The Email Sender ---
EmailSendAgent = LlmAgent(
    name="EmailSendAgent",
    
    model=MODEL_NAME,
    tools=[send_email],
    instruction=(
        "You are a specialist. Your ONLY job is to send an email. "
        "When you are called, you must use the `send_email` tool."
    )
)