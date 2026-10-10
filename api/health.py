"""
Vercel Serverless Function for /api/health
Handles /api/health, /api/health.py, /health, and root GET paths.
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from backend.app.main import app, health_check

@app.api_route("/api/health.py", methods=["GET"], include_in_schema=False)
@app.api_route("/api/health", methods=["GET"], include_in_schema=False)
@app.api_route("/health", methods=["GET"], include_in_schema=False)
@app.api_route("/", methods=["GET"], include_in_schema=False)
def handle_health_endpoint():
    return health_check()
