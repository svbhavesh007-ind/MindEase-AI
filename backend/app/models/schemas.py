"""
Pydantic Schemas for Request & Response validation
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class EmotionScore(BaseModel):
    emotion: str
    score: float = Field(..., ge=0.0, le=1.0)
    percentage: float

class EmotionAnalysis(BaseModel):
    primary_emotion: str
    confidence: float
    confidence_percentage: str
    emoji: str
    valence: str  # positive, negative, neutral
    intensity: str  # mild, moderate, intense
    actionable_theme: str
    breakdown: List[EmotionScore] = []

class CrisisResource(BaseModel):
    name: str
    country: str
    contact: str
    description: str
    link: Optional[str] = None

class CrisisAlert(BaseModel):
    is_crisis: bool
    risk_level: str  # none, low, moderate, severe
    triggers_detected: List[str] = []
    support_message: Optional[str] = None
    resources: List[CrisisResource] = []

class ChatMessage(BaseModel):
    role: str  # "user", "assistant", "system"
    content: str

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User's input text")
    history: List[ChatMessage] = []
    session_id: Optional[str] = None

class WellnessExercise(BaseModel):
    id: str
    title: str
    type: str  # breathing, grounding, affirmation, reflection
    duration: str
    steps: List[str]
    description: str

class ChatResponse(BaseModel):
    reply: str
    emotion: EmotionAnalysis
    crisis: CrisisAlert
    recommended_exercise: Optional[WellnessExercise] = None
    model_used: str

class AnalyzeEmotionRequest(BaseModel):
    text: str = Field(..., min_length=1)

class JournalEntry(BaseModel):
    id: Optional[str] = None
    title: str = "My Reflection"
    content: str
    timestamp: Optional[str] = None
    emotion: Optional[EmotionAnalysis] = None
    ai_reflection: Optional[str] = None
