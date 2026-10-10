import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.stdout.reconfigure(encoding="utf-8")

from starlette.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

# 1. Health check
h = client.get("/api/health")
print("Health Status:", h.status_code, h.json())

# 2. Analyze emotion direct endpoint
r_emo = client.post("/api/analyze-emotion", json={"text": "I feel so stressed and overwhelmed by exams"})
print("\nAnalyze Emotion Endpoint:", r_emo.json()["primary_emotion"], r_emo.json()["confidence_percentage"])

# 3. Chat endpoint
prompts = [
    "I feel happy",
    "I feel sad",
    "I am feeling so stressed about exams",
    "Thank you so much for helping me out today"
]

print("\n--- Chat Endpoint Tests ---")
for p in prompts:
    r = client.post("/api/chat", json={"message": p})
    data = r.json()
    emo = data["emotion"]
    print(f"'{p}' -> {emo['emoji']} {emo['primary_emotion'].upper()} ({emo['confidence_percentage']}) | Reply preview: {data['reply'][:60]}...")
