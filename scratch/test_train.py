import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB, ComplementNB
from sklearn.ensemble import VotingClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import accuracy_score, classification_report

df = pd.read_csv("c:/Users/svbha/Downloads/P2PL/data/mental_wellbeing_emotional_dataset.txt", sep="\t")
X = df["text"].astype(str)
y = df["emotion"].astype(str)

print(f"Dataset shape: {X.shape}")

# Model 1: Word + Char TF-IDF with Logistic Regression
p1 = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=1,
        max_features=5000
    )),
    ("clf", LogisticRegression(C=2.0, max_iter=1000, class_weight="balanced", random_state=42))
])

# Model 2: Word TF-IDF + ComplementNB
p2 = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=1
    )),
    ("clf", ComplementNB(alpha=0.5))
])

# Model 3: Tuned Logistic Regression with C=3.0
p3 = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=1,
        max_features=8000
    )),
    ("clf", LogisticRegression(C=3.5, max_iter=1000, random_state=42))
])

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for name, pipe in [("LogisticRegression (Balanced, C=2.0)", p1), ("ComplementNB (alpha=0.5)", p2), ("LogisticRegression (C=3.5)", p3)]:
    scores = cross_val_score(pipe, X, y, cv=cv, scoring="accuracy")
    print(f"{name}: CV Mean = {np.mean(scores):.4f} +/- {np.std(scores):.4f}")

p3.fit(X, y)
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

print("\n--- Predictions with P3 on tricky sentences ---")
for s in test_sentences:
    pred = p3.predict([s])[0]
    prob = np.max(p3.predict_proba([s])[0])
    print(f"'{s}' -> {pred} ({prob:.2f})")
