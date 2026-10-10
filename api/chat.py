"""
Vercel Serverless Function for /api/chat
Handles /api/chat, /api/chat.py, /chat, and root POST paths.
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from backend.app.main import app, chat
from backend.app.models.schemas import ChatRequest, ChatResponse

@app.api_route("/api/chat.py", methods=["POST", "OPTIONS"], include_in_schema=False)
@app.api_route("/api/chat", methods=["POST", "OPTIONS"], include_in_schema=False)
@app.api_route("/chat", methods=["POST", "OPTIONS"], include_in_schema=False)
@app.api_route("/", methods=["POST", "OPTIONS"], include_in_schema=False)
def handle_chat_endpoint(request: ChatRequest):
    return chat(request)
