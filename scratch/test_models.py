import os
import json
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

models_to_test = ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.8-27b"]

for m in models_to_test:
    print(f"\n--- Testing model: {m} ---")
    try:
        t0 = time.time()
        res = client.chat.completions.create(
            model=m,
            messages=[
                {"role": "system", "content": "You are a JSON-only emotion classifier. Return ONLY a JSON object."},
                {"role": "user", "content": "Text: 'I hate my boss, he is so unfair'\nAllowed emotions: [anger, anxiety, disgust, fear, gratitude, guilt, hope, joy, loneliness, love, neutral, sadness, shame, stress, surprise]\nRespond with JSON: {\"primary_emotion\": \"<name>\", \"confidence\": 0.95}"}
            ],
            temperature=0.0,
            max_tokens=100
        )
        print(f"Success in {time.time()-t0:.2f}s: {res.choices[0].message.content}")
    except Exception as e:
        print("Failed:", e)
