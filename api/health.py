"""
Vercel Serverless Function for /api/health
Direct endpoint routing for health check on Vercel.
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from backend.app.main import app, health_check

@app.get("/", include_in_schema=False)
def health_root():
    return health_check()
