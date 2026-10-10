"""
Vercel Serverless Function Entrypoint
Exposes the FastAPI ASGI app for Vercel Serverless Python runtime.
"""
import sys
from pathlib import Path

# Add project root to sys.path so backend and all submodules are importable
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Import the FastAPI application instance
from backend.app.main import app
