"""
MindEase Chatbot (Legacy & Streamlit Compatible Entrypoint)
Enhanced with real-time emotion recognition, safety guardrails, and modular backend integration.
To run: streamlit run chatbot.py
"""
import os
import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Import and execute the enhanced Streamlit app
import streamlit_app

if __name__ == "__main__":
    print("To launch the Streamlit interface, run:")
    print("  streamlit run chatbot.py")
    print("\nOr to launch the Full-Stack Web Application (FastAPI + Modern Web UI), run:")
    print("  python run.py")