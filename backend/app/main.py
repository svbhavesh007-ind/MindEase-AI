"""
MindEase FastAPI Application
Main backend entrypoint serving REST APIs and static frontend.
Compatible with local execution and Vercel Serverless Python runtime.
"""
import logging
from pathlib import Path
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from .config import APP_NAME, VERSION, DESCRIPTION, FRONTEND_DIR, STATIC_DIR, GROQ_API_KEY, GROQ_MODEL
from .models.schemas import (
    ChatRequest, ChatResponse, AnalyzeEmotionRequest, EmotionAnalysis,
    CrisisAlert, WellnessExercise, JournalEntry
)
from .ml.emotion_classifier import get_classifier
from .services.crisis_service import get_crisis_service, VERIFIED_RESOURCES
from .services.llm_service import get_llm_service
from .services.wellness_service import get_wellness_service

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("mindease")

app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    description=DESCRIPTION,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS configuration for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services on startup
classifier = get_classifier()
crisis_service = get_crisis_service()
llm_service = get_llm_service()
wellness_service = get_wellness_service()

# API Router to cleanly support both `/api/*` and direct route invocations
api_router = APIRouter()

@api_router.get("/health", tags=["System"])
def health_check():
    """Returns application health and model readiness status."""
    return {
        "status": "healthy",
        "app": APP_NAME,
        "version": VERSION,
        "model_classes_count": len(classifier.classes),
        "classes": classifier.classes,
        "llm_engine": f"Groq ({GROQ_MODEL})" if GROQ_API_KEY else "Intelligent Offline Empathy Engine"
    }

@api_router.post("/chat", response_model=ChatResponse, tags=["Conversational AI"])
def chat(request: ChatRequest):
    """
    Main dialogue endpoint:
    1. Evaluates crisis & safety signals
    2. Runs NLP Emotion Classification
    3. Recommends tailored mindfulness intervention
    4. Generates an empathetic LLM response
    """
    user_msg = request.message.strip()
    if not user_msg:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    # Step 1: Safety & Crisis Evaluation
    crisis_alert = crisis_service.evaluate(user_msg)

    # Step 2: Emotion Classification
    emotion_data = classifier.predict(user_msg)
    emotion_analysis = EmotionAnalysis(**emotion_data)

    # Step 3: Clinically-aligned Wellness Exercise
    recommended_exercise = None
    if emotion_analysis.primary_emotion != "neutral" and not crisis_alert.is_crisis:
        recommended_exercise = wellness_service.get_exercise_for_emotion(emotion_analysis.primary_emotion)

    # Step 4: Empathetic Dialogue Generation
    response_payload = llm_service.generate_response(
        user_message=user_msg,
        emotion_analysis=emotion_analysis,
        crisis_alert=crisis_alert,
        conversation_history=request.history
    )

    return ChatResponse(
        reply=response_payload["reply"],
        emotion=emotion_analysis,
        crisis=crisis_alert,
        recommended_exercise=recommended_exercise,
        model_used=response_payload["model_used"]
    )

@api_router.post("/analyze-emotion", response_model=EmotionAnalysis, tags=["NLP Analytics"])
def analyze_emotion(req: AnalyzeEmotionRequest):
    """Evaluates emotional distribution, valence, and intensity for any given text."""
    data = classifier.predict(req.text)
    return EmotionAnalysis(**data)

@api_router.get("/wellness/exercises", tags=["Wellness Toolkit"])
def list_exercises():
    """Returns all therapeutic guided mindfulness and grounding exercises."""
    return wellness_service.get_all_exercises()

@api_router.get("/wellness/affirmation", tags=["Wellness Toolkit"])
def get_affirmation(emotion: str = "neutral"):
    """Generates an emotion-attuned affirmation."""
    return {
        "emotion": emotion,
        "affirmation": wellness_service.get_affirmation(emotion)
    }

@api_router.get("/crisis-resources", tags=["Safety"])
def get_crisis_resources():
    """Returns verified 24/7 mental health emergency helpline numbers."""
    return VERIFIED_RESOURCES

@api_router.post("/journal", tags=["Wellness Toolkit"])
def process_journal_entry(entry: JournalEntry):
    """Analyzes a journal reflection, extracts emotion, and returns empathetic insights."""
    emotion_data = classifier.predict(entry.content)
    analysis = EmotionAnalysis(**emotion_data)
    
    # Generate warm reflective affirmation
    affirmation = wellness_service.get_affirmation(analysis.primary_emotion)
    ai_reflection = (
        f"Thank you for journaling your thoughts. I sense a feeling of {analysis.emoji} {analysis.primary_emotion.upper()} "
        f"in your reflection. Remember: {affirmation}"
    )

    entry.emotion = analysis
    entry.ai_reflection = ai_reflection
    return entry

# Mount API Router with both `/api` prefix and root so any Vercel URL rewrite succeeds seamlessly
app.include_router(api_router, prefix="/api")
app.include_router(api_router)

# Static Frontend mounting (supports local execution and standalone server)
target_static = STATIC_DIR if STATIC_DIR.exists() else FRONTEND_DIR
if target_static.exists():
    app.mount("/static", StaticFiles(directory=target_static), name="static")

    @app.get("/", include_in_schema=False)
    async def serve_index():
        index_file = target_static / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return JSONResponse({"status": "online", "message": "MindEase Backend is Running"})

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_frontend(full_path: str):
        if full_path.startswith("api/") or full_path == "api":
            raise HTTPException(status_code=404, detail="API endpoint not found")
        file_path = target_static / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        index_file = target_static / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return JSONResponse({"status": "online", "message": "MindEase Backend is Running"})
