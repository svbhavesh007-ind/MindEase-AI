import sys
import json
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def test_chat(prompt):
    url = "http://127.0.0.1:8000/api/chat"
    payload = json.dumps({"message": prompt}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print("\n" + "="*50)
        print(f"USER PROMPT: '{prompt}'")
        emo = data["emotion"]
        print(f"DETECTED EMOTION: {emo['emoji']} {emo['primary_emotion'].upper()} ({emo['confidence_percentage']})")
        print(f"VALENCE: {emo['valence']} | THEME: {emo['actionable_theme']}")
        if data.get("recommended_exercise"):
            print(f"RECOMMENDED EXERCISE: {data['recommended_exercise']['title']}")
        print(f"CRISIS DETECTED: {data['crisis']['is_crisis']}")
        print(f"MODEL USED: {data['model_used']}")
        print(f"REPLY:\n{data['reply']}")
        print("="*50)

if __name__ == "__main__":
    test_chat("I am feeling super anxious about my college exams tomorrow and my heart is racing.")
    test_chat("I got selected for the internship! I cannot stop smiling!")
    test_chat("I feel so lonely in my hostel room, no one talks to me.")
