import os
import json
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
print("API Key exists:", bool(api_key))

client = Groq(api_key=api_key)

test_sentences = [
    "I am feeling so stressed about exams",
    "I feel sad",
    "I feel happy",
    "I hate my boss, he is so unfair",
    "I just got accepted into my dream university!",
    "I feel like I'm not good enough and I'm a failure",
    "I'm terrified about tomorrow",
    "Thank you so much for being there for me",
    "Just checking in, had lunch and now working",
    "I feel so guilty for yelling at my sister",
    "I don't know what to do, my heart is pounding and I can't breathe",
    "Nobody cares about me, I have nobody to talk to",
    "I believe things will get better soon",
    "I love spending time with my puppy"
]

classes = ["anger", "anxiety", "disgust", "fear", "gratitude", "guilt", "hope", "joy", "loneliness", "love", "neutral", "sadness", "shame", "stress", "surprise"]

prompt_template = """You are an expert psychological emotion classifier.
Classify the emotion of this text: "{text}"
Allowed emotions: {classes}

Respond ONLY in valid JSON format:
{{
  "primary_emotion": "<one of allowed emotions>",
  "confidence": <float 0.5 to 0.99>,
  "valence": "<positive, negative, or neutral>",
  "intensity": "<mild, moderate, or intense>",
  "breakdown": [
     {{"emotion": "<name>", "score": <float>}},
     {{"emotion": "<name>", "score": <float>}},
     {{"emotion": "<name>", "score": <float>}}
  ]
}}"""

for s in test_sentences[:5]:
    t0 = time.time()
    try:
        res = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": prompt_template.format(text=s, classes=classes)}],
            temperature=0.0,
            max_tokens=200,
            response_format={"type": "json_object"}
        )
        elapsed = time.time() - t0
        content = res.choices[0].message.content
        data = json.loads(content)
        print(f"[{elapsed:.2f}s] '{s}' -> {data.get('primary_emotion')} ({data.get('confidence')})")
    except Exception as e:
        print("Error:", e)
