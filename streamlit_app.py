"""
MindEase Streamlit Edition
Enhanced emotion-aware mental wellness companion for Streamlit evaluation.
Run with: streamlit run streamlit_app.py
"""
import os
import sys
from pathlib import Path
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

# Ensure project root is in path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Load .env
load_dotenv(BASE_DIR / ".env")

from backend.app.ml.emotion_classifier import get_classifier
from backend.app.services.crisis_service import get_crisis_service
from backend.app.services.wellness_service import get_wellness_service
from backend.app.services.llm_service import get_llm_service
from backend.app.models.schemas import ChatMessage, EmotionAnalysis, CrisisAlert

# Page Configuration
st.set_page_config(
    page_title="MindEase — Emotion-Aware Mental Wellness",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Streamlit
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1, #14b8a6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 0.95rem;
        color: #94a3b8;
        margin-bottom: 20px;
    }
    .emotion-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 16px;
        background-color: #1e293b;
        border: 1px solid rgba(255,255,255,0.1);
        font-size: 0.82rem;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .crisis-card {
        padding: 16px;
        background-color: rgba(239, 68, 68, 0.15);
        border: 1px solid #ef4444;
        border-radius: 12px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Services
classifier = get_classifier()
crisis_service = get_crisis_service()
wellness_service = get_wellness_service()
llm_service = get_llm_service()

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "emotion_history" not in st.session_state:
    st.session_state.emotion_history = []
if "dominant_emotion" not in st.session_state:
    st.session_state.dominant_emotion = "Neutral"

# Sidebar
with st.sidebar:
    st.title("🌱 MindEase Hub")
    st.caption("College Project Edition • Emotion-Aware AI")

    st.subheader("📊 Emotion Analytics")
    if st.session_state.emotion_history:
        latest_emotion = st.session_state.emotion_history[-1]
        st.metric(
            label="Current State",
            value=f"{latest_emotion['emoji']} {latest_emotion['primary_emotion'].capitalize()}",
            delta=f"{latest_emotion['confidence_percentage']} Confidence"
        )
        st.write(f"**Valence:** `{latest_emotion['valence'].capitalize()}` | **Intensity:** `{latest_emotion.get('intensity', 'moderate').capitalize()}`")
        st.write(f"**Focus:** {latest_emotion['actionable_theme']}")

        # Current message breakdown
        if "breakdown" in latest_emotion and latest_emotion["breakdown"]:
            st.caption("Active Message Emotion Distribution:")
            bd_df = pd.DataFrame(latest_emotion["breakdown"]).set_index("emotion")["percentage"]
            st.bar_chart(bd_df, height=160)

        # Session History Distribution Chart
        st.caption("Session Mood History:")
        emo_counts = pd.Series([e["primary_emotion"] for e in st.session_state.emotion_history]).value_counts()
        st.bar_chart(emo_counts, height=160)
    else:
        st.info("Start chatting to see your live emotional state and radar analysis.")

    st.divider()

    # Mindfulness Toolkit Expander
    with st.expander("🧘 4-7-8 Breathing Guide", expanded=False):
        st.markdown("""
        **Paced Relaxation Technique:**
        1. **Inhale** quietly through nose: **4 seconds**
        2. **Hold** breath gently: **7 seconds**
        3. **Exhale** completely through mouth: **8 seconds**
        *Repeat 4 times to calm your autonomic nervous system.*
        """)

    with st.expander("🚨 Emergency Crisis Helplines", expanded=False):
        st.markdown("""
        - **India (Tele-MANAS)**: `14416` (24/7 Free)
        - **India (KIRAN)**: `1800-599-0019`
        - **India (Vandrevala)**: `+91 9999 666 555`
        - **USA/Canada**: Call/Text `988`
        - **UK (Samaritans)**: `116 123`
        """)

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.emotion_history = []
        st.rerun()

# Main Header
st.markdown('<div class="main-header">MindEase: Mental Wellness Companion</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Emotion-Aware Natural Language Processing & Empathetic Conversational Agent</div>', unsafe_allow_html=True)

# Render Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("emotion"):
            emo = msg["emotion"]
            st.markdown(f'<div class="emotion-pill">{emo["emoji"]} {emo["primary_emotion"].upper()} ({emo["confidence_percentage"]})</div>', unsafe_allow_html=True)
        st.markdown(msg["content"])
        if msg.get("exercise"):
            ex = msg["exercise"]
            st.info(f"💡 **Recommended Exercise:** {ex['title']} — {ex['description']}")

# Chat Input
user_input = st.chat_input("How are you feeling right now? Share anything on your mind...")

if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Process
    with st.chat_message("assistant"):
        with st.spinner("Reflecting with empathy..."):
            # 1. Crisis Evaluation
            crisis = crisis_service.evaluate(user_input)

            # 2. Emotion Classification
            emotion_res = classifier.predict(user_input)
            emotion_analysis = EmotionAnalysis(**emotion_res)
            st.session_state.emotion_history.append(emotion_res)

            # 3. Recommended Exercise
            rec_exercise = None
            if emotion_analysis.primary_emotion != "neutral" and not crisis.is_crisis:
                rec_exercise = wellness_service.get_exercise_for_emotion(emotion_analysis.primary_emotion)

            # 4. Generate Empathetic Response
            chat_history_objs = [ChatMessage(role=m["role"], content=m["content"]) for m in st.session_state.messages[:-1]]
            llm_res = llm_service.generate_response(
                user_message=user_input,
                emotion_analysis=emotion_analysis,
                crisis_alert=crisis,
                conversation_history=chat_history_objs
            )

            # Display Crisis Alert Banner if triggered
            if crisis.is_crisis:
                st.error("🚨 Crisis Guardrail Alert: If you are in immediate danger or experiencing overwhelming thoughts, please contact emergency services or call **14416 (India)** / **988 (USA)** immediately.")

            # Display Emotion Pill
            st.markdown(
                f'<div class="emotion-pill">{emotion_analysis.emoji} {emotion_analysis.primary_emotion.upper()} ({emotion_analysis.confidence_percentage}) &bull; {emotion_analysis.actionable_theme}</div>',
                unsafe_allow_html=True
            )

            # Display reply
            st.markdown(llm_res["reply"])

            # Display exercise if recommended
            if rec_exercise:
                st.info(f"💡 **Recommended Practice:** {rec_exercise.title} ({rec_exercise.duration})\n\n{rec_exercise.description}")

            # Store in session state
            st.session_state.messages.append({
                "role": "assistant",
                "content": llm_res["reply"],
                "emotion": emotion_res,
                "exercise": rec_exercise.model_dump() if rec_exercise else None
            })
