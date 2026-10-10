import os
import json
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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
    "I love spending time with my puppy",
    "The way people gossip about others behind their back is sickening",
    "I did not expect to win first place at all, wow!"
]

classes = ["anger", "anxiety", "disgust", "fear", "gratitude", "guilt", "hope", "joy", "loneliness", "love", "neutral", "sadness", "shame", "stress", "surprise"]

prompt = """You are a clinical-grade emotion classifier.
Classify the following text into exactly one primary emotion from this list:
{classes}

Text: "{text}"

Respond ONLY with valid JSON:
{{
  "primary_emotion": "<emotion from list>",
  "confidence": <float between 0.70 and 0.99>,
  "secondary_emotion": "<emotion from list>",
  "valence": "<positive, negative, or neutral>",
  "intensity": "<mild, moderate, or intense>"
}}"""

for s in test_sentences:
    t0 = time.time()
    res = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[{"role": "user", "content": prompt.format(classes=classes, text=s)}],
        temperature=0.0,
        max_tokens=120,
        response_format={"type": "json_object"}
    )
    data = json.loads(res.choices[0].message.content)
    print(f"[{time.time()-t0:.2f}s] '{s}' -> {data['primary_emotion']} ({data['confidence']}) [{data.get('intensity')}]")
