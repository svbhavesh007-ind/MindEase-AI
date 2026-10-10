"""
Vercel Serverless Function for /api/chat
Direct endpoint routing for Vercel without relying on rewrites.
"""
import sys
from pathlib import Path

# Add project root to sys.path so backend and all submodules are importable
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from backend.app.main import app, chat
from backend.app.models.schemas import ChatRequest, ChatResponse

# Register root POST handler on app in case Vercel passes stripped path "/" to this function
@app.post("/", response_model=ChatResponse, include_in_schema=False)
def chat_root(request: ChatRequest):
    return chat(request)
