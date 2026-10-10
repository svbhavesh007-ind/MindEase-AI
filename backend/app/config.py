"""
Application Configuration
Handles environment variables, file paths, and project settings.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = BASE_DIR / "backend"
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
FRONTEND_DIR = BASE_DIR / "frontend"
PUBLIC_DIR = BASE_DIR / "public"
STATIC_DIR = PUBLIC_DIR if PUBLIC_DIR.exists() else FRONTEND_DIR

# Load .env from project root
load_dotenv(BASE_DIR / ".env")

# Settings
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
PORT = int(os.getenv("PORT", "8000"))
HOST = os.getenv("HOST", "127.0.0.1")
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")

# Dataset and Model paths
DATASET_PATH = DATA_DIR / "mental_wellbeing_emotional_dataset.txt"
if not DATASET_PATH.exists():
    DATASET_PATH = BASE_DIR / "mental wellbeing emotional dataset.txt"

MODEL_FILE = MODELS_DIR / "emotion_classifier.joblib"
VECTORIZER_FILE = MODELS_DIR / "tfidf_vectorizer.joblib"
METRICS_FILE = MODELS_DIR / "evaluation_metrics.json"

# App Metadata
APP_NAME = "MindEase: Emotion-Aware Mental Wellness Companion"
VERSION = "2.0.0"
DESCRIPTION = "An emotion-aware AI mental wellness companion powered by NLP classification, empathetic LLM orchestration, and crisis intervention protocols."
