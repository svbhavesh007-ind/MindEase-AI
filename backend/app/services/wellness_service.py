"""
Wellness & Mindfulness Toolkit Service
Provides guided exercises (4-7-8 breathing, 5-4-3-2-1 grounding, self-compassion),
affirmations, and mood journal insights.
"""
from typing import Dict, Any, List, Optional
from ..models.schemas import WellnessExercise

WELLNESS_EXERCISES: Dict[str, WellnessExercise] = {
    "breathing_478": WellnessExercise(
        id="breathing_478",
        title="4-7-8 Relaxing Breath",
        type="breathing",
        duration="3 minutes",
        description="A scientifically proven technique to stimulate your parasympathetic nervous system, easing anxiety and racing thoughts.",
        steps=[
            "Find a comfortable position and place the tip of your tongue against the ridge behind your upper front teeth.",
            "Exhale completely through your mouth with a soft whoosh sound.",
            "Close your mouth and inhale quietly through your nose for 4 counts.",
            "Hold your breath gently for a count of 7.",
            "Exhale completely through your mouth for 8 counts, releasing all body tension.",
            "Repeat this cycle 4 times."
        ]
    ),
    "grounding_54321": WellnessExercise(
        id="grounding_54321",
        title="5-4-3-2-1 Sensory Grounding",
        type="grounding",
        duration="4 minutes",
        description="Anchors your mind to the physical present when experiencing panic, fear, or mental overload.",
        steps=[
            "Look around and name 5 things you can SEE (e.g., a shadow, the floor texture, a lamp).",
            "Touch and notice 4 things you can FEEL (e.g., the chair supporting you, fabric of your shirt).",
            "Listen closely and identify 3 things you can HEAR (e.g., a hum of the fan, distant birds, your breath).",
            "Identify 2 things you can SMELL around you (e.g., fresh air, coffee, paper).",
            "Acknowledge 1 good thing you can TASTE or say one kind sentence to yourself."
        ]
    ),
    "self_compassion": WellnessExercise(
        id="self_compassion",
        title="Self-Compassion Pause",
        type="reflection",
        duration="3 minutes",
        description="Designed for moments of shame, sadness, or harsh self-criticism.",
        steps=[
            "Gently place one or both hands over your heart or on your chest, feeling the warmth of your hands.",
            "Acknowledge your pain: 'This is a moment of suffering or difficulty.'",
            "Remember common humanity: 'Suffering and feeling inadequate is part of being human. I am not uniquely broken.'",
            "Offer kindness: 'May I be patient with myself. May I give myself the compassion I need right now.'"
        ]
    ),
    "progressive_muscle": WellnessExercise(
        id="progressive_muscle",
        title="Quick Tension Release (PMR)",
        type="relaxation",
        duration="4 minutes",
        description="Physically discharges cortisol and adrenaline triggered by frustration or anger.",
        steps=[
            "Clench your fists tightly for 5 seconds... notice the strain... then suddenly release completely.",
            "Hunch your shoulders up towards your ears for 5 seconds... and let them drop down heavily.",
            "Tighten your jaw and facial muscles... hold... and let your mouth fall slack.",
            "Take one deep, slow sigh out, allowing your entire body to sink into relaxation."
        ]
    ),
    "gratitude_boost": WellnessExercise(
        id="gratitude_boost",
        title="Three Good Anchors",
        type="affirmation",
        duration="2 minutes",
        description="Amplifies positive neuroplasticity and emotional resilience.",
        steps=[
            "Bring to mind one small pleasant thing that happened today (even a warm sip of tea).",
            "Reflect on one person whose existence has made your life a little better.",
            "Identify one quality or effort in yourself that you appreciate today.",
            "Let the warm sensation linger in your chest for 3 slow breaths."
        ]
    )
}

AFFIRMATIONS_BY_EMOTION = {
    "anxiety": [
        "I am safe in this present moment. My thoughts are just thoughts, not emergencies.",
        "I don't have to figure everything out today. Taking it one breath at a time is enough.",
        "My nervous system knows how to return to peace. I allow my shoulders to drop."
    ],
    "sadness": [
        "It is okay to not be okay right now. Giving myself space to feel is strength.",
        "This heavy cloud will pass, just as every weather system does.",
        "I treat myself with the same gentle care I would offer a dear friend."
    ],
    "stress": [
        "I can only do what I can do today, and that is worthy of respect.",
        "Rest is not a reward I must earn; it is a necessity my mind and body deserve.",
        "I pause, unclench my jaw, and release what I cannot control."
    ],
    "loneliness": [
        "Even when I feel disconnected, my presence in this world matters.",
        "Solitude can be a gentle space to befriend myself.",
        "There are people in this world who will cherish who I truly am."
    ],
    "anger": [
        "My anger is telling me something matters. I can honor my boundaries without letting fury consume me.",
        "I choose to respond with calm authority rather than react in heat.",
        "I breathe out tension and breathe in clarity."
    ],
    "guilt": [
        "I made decisions based on who I was then; I am allowed to grow and forgive myself.",
        "Making a mistake does not make me a bad person. I focus on constructive healing."
    ],
    "shame": [
        "My self-worth is inherent. It is never determined by grades, mistakes, or other people's opinions.",
        "I am worthy of love, dignity, and belonging exactly as I am."
    ],
    "joy": [
        "I fully receive this moment of happiness and celebrate my life.",
        "Joy is my natural birthright, and I let it radiate through me."
    ],
    "hope": [
        "I trust that small consistent steps lead to beautiful horizons.",
        "Every sunrise brings a new possibility for renewal."
    ]
}

class WellnessService:
    def get_exercise_for_emotion(self, emotion: str) -> WellnessExercise:
        """Returns the most clinically indicated exercise for the current emotion."""
        if emotion in ["anxiety", "fear"]:
            return WELLNESS_EXERCISES["grounding_54321"]
        elif emotion in ["stress", "neutral"]:
            return WELLNESS_EXERCISES["breathing_478"]
        elif emotion in ["sadness", "guilt", "shame"]:
            return WELLNESS_EXERCISES["self_compassion"]
        elif emotion == "anger":
            return WELLNESS_EXERCISES["progressive_muscle"]
        else:
            return WELLNESS_EXERCISES["gratitude_boost"]

    def get_all_exercises(self) -> List[WellnessExercise]:
        return list(WELLNESS_EXERCISES.values())

    def get_affirmation(self, emotion: str) -> str:
        options = AFFIRMATIONS_BY_EMOTION.get(emotion.lower(), [
            "You are doing your best, and that is genuinely enough.",
            "Take one gentle breath at a time. You are safe.",
            "Be kind to yourself today."
        ])
        import random
        return random.choice(options)

wellness_service_instance = None

def get_wellness_service() -> WellnessService:
    global wellness_service_instance
    if wellness_service_instance is None:
        wellness_service_instance = WellnessService()
    return wellness_service_instance
