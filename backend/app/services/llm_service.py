"""
LLM Orchestration & Empathetic Response Service
Integrates Groq API with robust fallback to a local psychological empathy engine.
Ensures zero-downtime, emotion-conditioned mental health dialogues.
"""
import logging
import random
from typing import List, Dict, Any, Optional
from groq import Groq

from ..config import GROQ_API_KEY, GROQ_MODEL, DATASET_PATH
from ..models.schemas import ChatMessage, EmotionAnalysis, CrisisAlert

logger = logging.getLogger(__name__)

# Load Knowledge Base examples for context and fallback
def load_kb_examples() -> Dict[str, List[Dict[str, str]]]:
    examples_by_emotion: Dict[str, List[Dict[str, str]]] = {}
    try:
        if DATASET_PATH.exists():
            import pandas as pd
            df = pd.read_csv(DATASET_PATH, sep="\t", engine="python")
            if "emotion" not in df.columns or "text" not in df.columns:
                df = pd.read_csv(DATASET_PATH, sep=",", engine="python")
            for _, row in df.iterrows():
                emo = str(row["emotion"]).strip().lower()
                txt = str(row["text"]).strip()
                resp = str(row.get("response", "")).strip()
                if emo not in examples_by_emotion:
                    examples_by_emotion[emo] = []
                examples_by_emotion[emo].append({"text": txt, "response": resp})
    except Exception as e:
        logger.warning(f"Could not load KB examples: {e}")
    return examples_by_emotion

KB_EXAMPLES = load_kb_examples()

FALLBACK_TEMPLATES = {
    "anxiety": [
        "It sounds like your mind is running in high gear right now and carrying a heavy load. Let's pause for a second — your body is completely safe right here. Would it help to gently untangle what's feeling most overwhelming first?",
        "Anxiety can make everything feel urgent and catastrophic at the exact same time. Take a deep, slow breath with me. You don't have to resolve everything today. What is one small thing on your plate we can look at together?",
        "I can sense the tension and racing thoughts behind your words. Feeling on edge is exhausting. Let's take it one step at a time — what do you feel would bring you even 1% more ease right now?"
    ],
    "sadness": [
        "I'm really sorry things are feeling so heavy right now. It is completely okay to feel sad, and you don't have to put on a brave face here. I'm sitting with you — do you want to talk more about what's on your heart?",
        "That sounds deeply disheartening. Give yourself permission to rest and feel whatever is coming up without judging yourself. I am right here listening whenever you're ready to share.",
        "Your feelings are completely valid. When sadness sets in, it can make everything feel grey and lonely. Thank you for opening up to me — remember you don't have to carry this completely alone."
    ],
    "stress": [
        "That is a tremendous amount of pressure to juggle at once. It's completely natural to feel stretched to your limit. Let's see if we can take a step back: what is the single most demanding item, and what can wait?",
        "Feeling burnt out and overloaded is your mind's way of signaling it needs a breather. You've been pushing yourself hard. Can we take three slow, deep breaths together before doing anything else?",
        "It sounds like deadlines and expectations are closing in on you. Remember that your peace of mind is worth protecting. What is one responsibility you can give yourself permission to step away from today?"
    ],
    "anger": [
        "It makes total sense that you'd feel furious about that. When your boundaries or efforts are disregarded, anger is a very healthy signal. Would it feel good to vent more of what happened, or would you like to think about how to handle it?",
        "I hear how frustrating and unfair that situation is. Your anger is valid. Let's let the heat breathe for a moment so it doesn't hurt you inside — what felt like the most disrespectful part?",
        "That would make anyone's blood boil. You have every right to feel annoyed. I'm here to listen to all of it without any judgment."
    ],
    "loneliness": [
        "Feeling isolated or like no one truly understands is one of the hardest human experiences. I'm so glad you reached out and told me. Even through this screen, you are heard and valued today.",
        "It hurts when connection feels out of reach, especially when surrounded by people. You are not invisible here. What kind of connection or conversation are you craving most lately?",
        "Loneliness can whisper that nobody cares, but that's the pain talking, not the truth. I'm right here with you. How has your day felt so far?"
    ],
    "joy": [
        "That is so wonderful to hear! Your excitement is truly contagious, and you deserve to celebrate every bit of this win. How does it feel to see your effort pay off?",
        "I love this for you! Taking the time to savor good news is so nourishing for your wellbeing. Tell me more — what was the best part of the whole experience?",
        "That's fantastic! Celebrating these joyful milestones builds real resilience. Thank you so much for sharing your happiness with me today!"
    ],
    "gratitude": [
        "Noticing these moments of kindness and support is such a beautiful strength. Practicing gratitude like this brings genuine groundedness. Who or what else has brought a warm spark into your life recently?",
        "It's heartwarming to read this. Recognizing the good people and circumstances around you is so healing. How does holding onto that appreciation make you feel right now?"
    ],
    "hope": [
        "I admire your resilience and optimism. Holding onto hope, especially when things have been challenging, is powerful. What are you most looking forward to as you move forward?",
        "That spark of hope is such a guiding light. Believing that brighter chapters are ahead is half the journey. What's one small step you want to take towards that vision?"
    ],
    "fear": [
        "That sounds frightening to face, and your fear is understandable. Let's ground ourselves in this exact moment: right here, right now, you are safe. What part of the situation is causing you the most dread?",
        "Fear can feel paralyzing, but you don't have to face it by yourself. Let's break the scary scenario down into bite-sized pieces so it doesn't loom so big. What would help you feel a bit safer?"
    ],
    "guilt": [
        "It sounds like you're carrying a very heavy burden of guilt and being very hard on yourself. We are all human, and mistakes are part of learning. What would you say to a friend who was in your exact shoes right now?",
        "Guilt shows that you have a compassionate conscience, but holding onto self-blame won't heal the past. Can you offer yourself a little bit of the grace you so readily give to others?"
    ],
    "shame": [
        "Thank you for trusting me with something that feels so raw and vulnerable. Shame tells us we aren't good enough, but your worth as a person is unconditional. You deserve compassion, especially from yourself today.",
        "Feeling exposed or embarrassed is so painful, but please remember that one moment or perceived flaw does not define who you are. I'm right here with you with zero judgment."
    ],
    "neutral": [
        "Thank you for checking in today. How is the rest of your day shaping up? If there's anything on your mind — big or small — I'm here to chat about it.",
        "Got it! Sometimes having a quiet, routine day is just what we need. How are you feeling physically and mentally today?"
    ]
}

class LLMService:
    def __init__(self):
        self.client: Optional[Groq] = None
        self._init_groq_client()

    def _init_groq_client(self):
        """Initializes Groq client if an API key is provided."""
        if GROQ_API_KEY and len(GROQ_API_KEY) > 10:
            try:
                self.client = Groq(api_key=GROQ_API_KEY)
                logger.info("Groq LLM Client initialized successfully.")
            except Exception as e:
                logger.warning(f"Could not initialize Groq client: {e}")
                self.client = None
        else:
            logger.info("No Groq API key found. Operating in Intelligent Offline Empathy Mode.")

    def generate_response(
        self,
        user_message: str,
        emotion_analysis: EmotionAnalysis,
        crisis_alert: CrisisAlert,
        conversation_history: List[ChatMessage]
    ) -> Dict[str, str]:
        """
        Generates an empathetic response conditioned on the detected emotional state.
        Prioritizes Groq LLM and falls back seamlessly to the Psychological Counseling Engine.
        """
        # If severe crisis is detected, provide immediate de-escalation response
        if crisis_alert.is_crisis:
            return {
                "reply": (
                    f"{crisis_alert.support_message}\n\n"
                    "Please connect with one of these confidential, 24/7 helplines right now:\n"
                    "• **Tele-MANAS (India)**: Call **14416** or **1800-891-4416**\n"
                    "• **KIRAN Helpline**: Call **1800-599-0019**\n"
                    "• **Vandrevala Foundation**: Call or WhatsApp **+91 9999 666 555**\n"
                    "• **US / Canada**: Call or Text **988**\n"
                    "• **UK (Samaritans)**: Call **116 123**\n\n"
                    "I am here with you, but having a trained human counselor on the phone with you right now is the safest step. Please take this step for yourself."
                ),
                "model_used": "Crisis-Safety-Guardrail"
            }

        # Try Groq API if client exists
        if self.client:
            try:
                system_prompt = self._build_system_prompt(emotion_analysis)
                messages = [{"role": "system", "content": system_prompt}]

                # Include past turns (up to last 6 for context continuity)
                for msg in conversation_history[-6:]:
                    if msg.role in ["user", "assistant"]:
                        messages.append({"role": msg.role, "content": msg.content})

                # Append current user message
                messages.append({"role": "user", "content": user_message})

                completion = self.client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=450
                )
                reply = completion.choices[0].message.content.strip()
                return {
                    "reply": reply,
                    "model_used": f"Groq/{GROQ_MODEL}"
                }
            except Exception as e:
                logger.warning(f"Groq API call failed ({e}). Falling back to Offline Empathy Engine.")

        # Fallback to Psychological Empathy Engine
        reply = self._generate_offline_response(user_message, emotion_analysis)
        return {
            "reply": reply,
            "model_used": "MindEase-Offline-Empathy-Engine"
        }

    def _build_system_prompt(self, emotion_analysis: EmotionAnalysis) -> str:
        """
        Builds a rich, emotion-conditioned prompt instructing the LLM on clinical empathy principles.
        """
        primary = emotion_analysis.primary_emotion
        valence = emotion_analysis.valence
        confidence = emotion_analysis.confidence_percentage
        theme = emotion_analysis.actionable_theme

        return f"""You are MindEase, an empathetic, emotionally-aware AI companion specialized in mental wellbeing.
Your purpose is to offer compassionate, non-clinical, validating, and grounding emotional support.

CURRENT USER EMOTION ANALYSIS:
- Primary Detected Emotion: {primary.upper()} ({confidence} confidence)
- Emotional Valence: {valence.upper()}
- Psychological Intervention Theme: {theme}

CRITICAL COMMUNICATION GUIDELINES:
1. VALIDATE & NORMALIZE: Acknowledge and validate the user's specific feelings first. Never say "just be positive" or dismiss their experience.
2. REFLECTIVE LISTENING: Gently mirror the essence of what they shared so they feel heard.
3. CONVERSATIONAL & WARM: Keep responses concise (2 to 4 short paragraphs), gentle, and human. Avoid overly clinical therapy jargon.
4. GENTLE EXPLORATION: End with a soft, open-ended question or offer a gentle grounding idea (e.g. taking a breath, taking things one step at a time).
5. NON-PRESCRIPTIVE: You are a supportive peer and listener, not a medical doctor. Do not diagnose conditions or prescribe medications.
"""

    def _generate_offline_response(self, user_message: str, emotion_analysis: EmotionAnalysis) -> str:
        """
        Generates contextually matched empathetic responses using knowledge base and counseling patterns.
        """
        primary = emotion_analysis.primary_emotion.lower()
        options = FALLBACK_TEMPLATES.get(primary, FALLBACK_TEMPLATES["neutral"])

        # Check if we have sample dataset replies for this emotion
        kb_matches = KB_EXAMPLES.get(primary, [])
        if kb_matches and random.random() < 0.35:
            sample_reply = random.choice(kb_matches)["response"]
            if sample_reply and len(sample_reply) > 20:
                return sample_reply

        return random.choice(options)

# Singleton
llm_service_instance = None

def get_llm_service() -> LLMService:
    global llm_service_instance
    if llm_service_instance is None:
        llm_service_instance = LLMService()
    return llm_service_instance
