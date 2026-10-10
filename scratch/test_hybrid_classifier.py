import os
import re
import json
import time
from typing import Dict, Any, List, Tuple
from functools import lru_cache
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from groq import Groq
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

load_dotenv("c:/Users/svbha/Downloads/P2PL/.env")

TAXONOMY = {
    "joy": {"emoji": "✨", "valence": "positive", "theme": "Celebration & Strength-Spotting"},
    "gratitude": {"emoji": "🙏", "valence": "positive", "theme": "Appreciation & Connection"},
    "hope": {"emoji": "🌱", "valence": "positive", "theme": "Forward Vision & Resilience"},
    "love": {"emoji": "💖", "valence": "positive", "theme": "Bonding & Warmth"},
    "surprise": {"emoji": "😲", "valence": "neutral", "theme": "Processing & Grounding"},
    "neutral": {"emoji": "💬", "valence": "neutral", "theme": "Daily Check-in & Curiosity"},
    "sadness": {"emoji": "🌧️", "valence": "negative", "theme": "Emotional Comfort & Gentle Presence"},
    "anxiety": {"emoji": "⚡", "valence": "negative", "theme": "Somatic Calm & Nervous System Reset"},
    "fear": {"emoji": "🛡️", "valence": "negative", "theme": "Safety, Validation & Reassurance"},
    "stress": {"emoji": "🌪️", "valence": "negative", "theme": "De-escalation & Boundary Setting"},
    "anger": {"emoji": "🔥", "valence": "negative", "theme": "Healthy Release & Reframing"},
    "loneliness": {"emoji": "🌌", "valence": "negative", "theme": "Belonging & Meaningful Connection"},
    "guilt": {"emoji": "🥀", "valence": "negative", "theme": "Forgiveness & Amends"},
    "shame": {"emoji": "🩹", "valence": "negative", "theme": "Radical Acceptance & Self-Worth"},
    "disgust": {"emoji": "🛑", "valence": "negative", "theme": "Values Alignment & Distance"}
}

ALL_CLASSES = list(TAXONOMY.keys())

# Train local ML
df = pd.read_csv("c:/Users/svbha/Downloads/P2PL/data/mental_wellbeing_emotional_dataset.txt", sep="\t")
ml_pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, min_df=1, max_features=8000)),
    ("clf", LogisticRegression(C=3.5, max_iter=1000, random_state=42))
])
ml_pipeline.fit(df["text"].astype(str), df["emotion"].astype(str))
classes = list(ml_pipeline.classes_)

# Groq Client
api_key = os.getenv("GROQ_API_KEY", "")
groq_client = Groq(api_key=api_key) if api_key else None

def classify_text(text: str) -> Dict[str, Any]:
    text_clean = text.strip()
    if not text_clean:
        return {"primary_emotion": "neutral", "confidence": 0.5, "source": "empty"}

    # 1. Try Groq fast LLM (qwen3.8-27b or openai/gpt-oss-120b)
    if groq_client:
        try:
            t0 = time.time()
            prompt = f"""Classify the user's emotion into exactly one primary emotion from:
{ALL_CLASSES}

Text: "{text_clean}"

Return valid JSON ONLY:
{{
  "primary_emotion": "<emotion>",
  "confidence": <float 0.70 to 0.99>,
  "secondary_emotion": "<emotion>",
  "valence": "<positive, negative, or neutral>",
  "intensity": "<mild, moderate, or intense>"
}}"""
            res = groq_client.chat.completions.create(
                model="qwen/qwen3.8-27b",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=120,
                response_format={"type": "json_object"},
                timeout=2.0
            )
            raw = res.choices[0].message.content.strip()
            data = json.loads(raw)
            primary = data.get("primary_emotion", "").lower()
            if primary in TAXONOMY:
                conf = float(data.get("confidence", 0.90))
                return {
                    "primary_emotion": primary,
                    "confidence": conf,
                    "confidence_percentage": f"{round(conf * 100, 1)}%",
                    "source": f"Neural-Groq ({time.time()-t0:.2f}s)",
                    "intensity": data.get("intensity", "moderate"),
                    "valence": data.get("valence", TAXONOMY[primary]["valence"])
                }
        except Exception as e:
            # Fallback to local ML
            pass

    # 2. Local fallback ML
    probs = ml_pipeline.predict_proba([text_clean])[0]
    top_idx = int(np.argmax(probs))
    primary = classes[top_idx]
    conf = float(probs[top_idx])
    return {
        "primary_emotion": primary,
        "confidence": conf,
        "confidence_percentage": f"{round(conf * 100, 1)}%",
        "source": "Local-ML",
        "intensity": "moderate",
        "valence": TAXONOMY[primary]["valence"]
    }

test_set = [
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

print("Running test suite:")
for s in test_set:
    res = classify_text(s)
    print(f"'{s}' -> {res['primary_emotion'].upper()} ({res['confidence_percentage']}) [{res['source']}]")
