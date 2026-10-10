"""
Standalone ML Training and Evaluation Script
Used for generating model artifacts and printing academic evaluation metrics.
Run directly: python -m backend.app.ml.train
"""
import sys
import json
from pathlib import Path

# Ensure root is in path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from backend.app.ml.emotion_classifier import EmotionClassifier

def main():
    print("=" * 60)
    print("🧠 MindEase Emotion Classifier: Training & Evaluation")
    print("=" * 60)

    classifier = EmotionClassifier()
    print("[1/3] Loading dataset and vectorizing textual features...")
    df = classifier.load_dataset()
    print(f"      Total samples: {len(df)}")
    print(f"      Emotion distribution:\n{df['emotion'].value_counts().to_string()}")

    print("\n[2/3] Training TF-IDF + Calibrated Logistic Regression Model...")
    metrics = classifier.train_and_save()

    print("\n[3/3] Training & Cross-Validation Results:")
    print("-" * 60)
    print(f"• Stratified 3-Fold CV Accuracy: {metrics['cv_accuracy_mean'] * 100:.2f}% (±{metrics['cv_accuracy_std'] * 100:.2f}%)")
    print(f"• In-Sample Training Accuracy:   {metrics['train_accuracy'] * 100:.2f}%")
    print(f"• Number of Recognized Classes:  {metrics['num_classes']}")
    print("-" * 60)

    print("\nSample Inferences:")
    test_queries = [
        "I feel so overwhelmed with my exams and can't focus.",
        "I finally got the internship, I can't stop jumping around!",
        "I miss home and feel like no one here cares about me.",
        "My roommate ruined my laptop assignment and I am furious.",
        "I'm scared of what comes after graduation."
    ]

    for q in test_queries:
        res = classifier.predict(q)
        print(f"\nQuery: \"{q}\"")
        print(f"  -> Detected Emotion: {res['emoji']} {res['primary_emotion'].upper()} ({res['confidence_percentage']} confidence)")
        print(f"  -> Valence: {res['valence']} | Focus: {res['actionable_theme']}")

    print("\nModel saved successfully in /models directory.")
    print("=" * 60)

if __name__ == "__main__":
    main()
