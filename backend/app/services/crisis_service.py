"""
Crisis Intervention & Safety Triage Service
Detects signs of extreme distress, suicidal ideation, or self-harm.
Provides safety alerts, grounding interventions, and verified emergency helplines.
"""
import re
from typing import Dict, Any, List
from ..models.schemas import CrisisAlert, CrisisResource

CRISIS_PATTERNS = [
    # Suicidal ideation & self-harm
    r"\b(suicid(e|al)|kill\s+(my\s*self|me)|end\s+it\s+all|want\s+to\s+die|don't\s+want\s+to\s+live|better\s+off\s+dead)\b",
    r"\b(take\s+my\s+(own\s+)?life|hang\s+myself|cut\s+myself|slit\s+my|overdose|swallow\s+pills)\b",
    r"\b(disappear\s+forever|nobody\s+would\s+miss\s+me|no\s+reason\s+to\s+live|goodbye\s+everyone|ending\s+my\s+life)\b",
    r"\b(can't\s+take\s+this\s+pain\s+anymore|hurt\s+myself)\b"
]

HIGH_DISTRESS_PATTERNS = [
    r"\b(hopeless|worthless|can't\s+go\s+on|no\s+point\s+in\s+trying|give\s+up\s+on\s+life)\b",
    r"\b(severe\s+panic|can't\s+breathe|having\s+a\s+breakdown|losing\s+my\s+mind)\b"
]

VERIFIED_RESOURCES: List[CrisisResource] = [
    CrisisResource(
        name="Tele-MANAS (Govt of India)",
        country="India",
        contact="14416 / 1800-891-4416",
        description="24/7 free, confidential mental health tele-counseling in 20+ languages.",
        link="tel:14416"
    ),
    CrisisResource(
        name="KIRAN Mental Health Helpline",
        country="India",
        contact="1800-599-0019",
        description="Government 24/7 national helpline for anxiety, depression, and distress relief.",
        link="tel:18005990019"
    ),
    CrisisResource(
        name="Vandrevala Foundation",
        country="India",
        contact="+91 9999 666 555",
        description="Free, round-the-clock professional counseling and crisis support via call/WhatsApp.",
        link="tel:+919999666555"
    ),
    CrisisResource(
        name="988 Suicide & Crisis Lifeline",
        country="USA & Canada",
        contact="988",
        description="Call or text 988 anytime for free, confidential mental health crisis support.",
        link="tel:988"
    ),
    CrisisResource(
        name="Samaritans UK",
        country="UK & Ireland",
        contact="116 123",
        description="24/7 free emotional support helpline for anyone in distress.",
        link="tel:116123"
    ),
    CrisisResource(
        name="Befrienders Worldwide",
        country="International",
        contact="befrienders.org",
        description="Global network of emotional support helplines in over 32 countries.",
        link="https://www.befrienders.org"
    )
]

class CrisisService:
    def __init__(self):
        self.crisis_regex = [re.compile(p, re.IGNORECASE) for p in CRISIS_PATTERNS]
        self.distress_regex = [re.compile(p, re.IGNORECASE) for p in HIGH_DISTRESS_PATTERNS]

    def evaluate(self, text: str) -> CrisisAlert:
        """
        Scans text for critical keywords and returns risk level + emergency contacts.
        """
        if not text:
            return CrisisAlert(is_crisis=False, risk_level="none", triggers_detected=[], resources=[])

        detected_severe = []
        for regex in self.crisis_regex:
            match = regex.search(text)
            if match:
                detected_severe.append(match.group(0))

        if detected_severe:
            return CrisisAlert(
                is_crisis=True,
                risk_level="severe",
                triggers_detected=detected_severe,
                support_message=(
                    "I hear how deeply painful things feel right now, and I want you to know you are not alone. "
                    "Your life and safety matter immensely. Please reach out to someone who can support you right this second. "
                    "Free, confidential counselors are ready to listen 24/7."
                ),
                resources=VERIFIED_RESOURCES
            )

        detected_distress = []
        for regex in self.distress_regex:
            match = regex.search(text)
            if match:
                detected_distress.append(match.group(0))

        if detected_distress:
            return CrisisAlert(
                is_crisis=False,
                risk_level="moderate",
                triggers_detected=detected_distress,
                support_message=(
                    "You seem to be carrying a very heavy emotional load right now. "
                    "Take a slow breath. If you ever feel in danger or need someone to talk to right away, "
                    "support is always available."
                ),
                resources=VERIFIED_RESOURCES[:2]
            )

        return CrisisAlert(
            is_crisis=False,
            risk_level="none",
            triggers_detected=[],
            resources=[]
        )

# Global singleton
crisis_service_instance = None

def get_crisis_service() -> CrisisService:
    global crisis_service_instance
    if crisis_service_instance is None:
        crisis_service_instance = CrisisService()
    return crisis_service_instance
