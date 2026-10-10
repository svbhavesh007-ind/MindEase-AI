#!/usr/bin/env bash
echo "========================================================"
echo "  Starting MindEase: Emotion-Aware Mental Wellness Companion"
echo "========================================================"
echo ""

if [ -f "venv/bin/python" ]; then
    venv/bin/python run.py
else
    python3 run.py
fi
