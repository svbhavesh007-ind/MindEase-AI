import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Ensure stdout handles utf-8 on Windows
sys.stdout.reconfigure(encoding="utf-8")

from backend.app.ml.emotion_classifier import get_classifier

clf = get_classifier()

test_cases = [
    "I feel happy",
    "I feel sad",
    "I am stressed about exams",
    "I am so anxious and my heart is beating fast",
    "I am terrified of failing",
    "I hate my roommate, he stole my food",
    "I feel lonely, nobody talks to me",
    "Thank you so much for your support",
    "I love my dog, he is the best",
    "I believe things will be better soon",
    "I feel guilty for snapping at my mom",
    "I feel like an embarrassed failure in front of everyone",
    "That disgusting behavior makes me sick",
    "I was completely shocked by the test results",
    "hello how are you",
    "Just walking to class today",
    "I am not happy with my grades",
    "My hands are shaking and I am panicking"
]

print(f"=== TESTING EMOTION CLASSIFIER ({len(test_cases)} tests) ===")
for t in test_cases:
    res = clf.predict(t)
    print(f"{t:<55} -> {res['primary_emotion'].upper():<12} ({res['confidence_percentage']:<6}) [{res['actionable_theme']}]")
