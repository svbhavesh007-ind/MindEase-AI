"""
MindEase 2.0 Launcher
One-command launcher that initializes the ML model, starts the FastAPI server,
and opens the web interface in your default browser.
"""
import os
import sys
import time
import webbrowser
import threading
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Ensure Windows terminal prints UTF-8 correctly
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def ensure_model_trained():
    """Validates that ML model artifacts exist, training them automatically if needed."""
    from backend.app.config import MODEL_FILE
    from backend.app.ml.emotion_classifier import EmotionClassifier

    if not MODEL_FILE.exists():
        print("🧠 [MindEase ML] Initializing & training Emotion Classification Model on dataset...")
        classifier = EmotionClassifier()
        metrics = classifier.train_and_save()
        print(f"✅ [MindEase ML] Model trained with {metrics['num_classes']} emotion classes!")
    else:
        print("✅ [MindEase ML] Pretrained emotion classification model ready.")

def open_browser(url: str, delay: float = 1.2):
    """Opens web browser after server initializes."""
    def _open():
        time.sleep(delay)
        print(f"🌐 Opening MindEase in your default browser: {url}")
        webbrowser.open(url)
    threading.Thread(target=_open, daemon=True).start()

def main():
    print("=" * 65)
    print("   🌱 MindEase: Emotion-Aware Mental Wellness Companion")
    print("      Full-Stack AI Project for College Evaluation & GitHub")
    print("=" * 65)

    ensure_model_trained()

    from backend.app.config import HOST, PORT, GROQ_API_KEY, GROQ_MODEL
    url = f"http://{HOST}:{PORT}"

    print(f"\n📡 Server starting at: {url}")
    print(f"📖 Swagger API Docs:  {url}/api/docs")
    print(f"🤖 LLM Engine:        {'Groq (' + GROQ_MODEL + ')' if GROQ_API_KEY else 'Intelligent Offline Empathy Mode'}")
    print("-" * 65)
    print("💡 Press Ctrl + C to stop the server at any time.\n")

    open_browser(url)

    import uvicorn
    uvicorn.run("backend.app.main:app", host=HOST, port=PORT, reload=False)

if __name__ == "__main__":
    main()
