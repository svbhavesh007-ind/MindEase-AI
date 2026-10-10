# 🚀 MindEase: Vercel Deployment Guide

This guide walks you through deploying the **MindEase Emotion-Aware Mental Wellness Companion** to **Vercel** as a full-stack serverless web application.

---

## 🏗️ Architecture Overview

The application is structured for Vercel's Serverless architecture:
- **Frontend** (`/public`): Static HTML, CSS, and Vanilla JS served automatically via Vercel's global Edge CDN with zero cold-start delay.
- **Backend API** (`/api/index.py`): FastAPI backend executed on Vercel's Python Serverless Runtime.
- **Routing** (`vercel.json`): Directs `/api/*` requests to `api/index.py` and serves UI files at the root domain (`/`).
- **Trained Model** (`/models/emotion_classifier.joblib`): Pre-trained model packaged with the deployment for instant offline/hybrid inference.

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure:
1. You have a free account on [Vercel](https://vercel.com).
2. You have a free account on [GitHub](https://github.com) (if deploying via Git).
3. You have your **Groq API Key** ready (`gsk_...`).

---

## 🌟 Method 1: Deploy via GitHub (Recommended)

This is the standard and most reliable method to deploy on Vercel with automatic continuous deployment (CI/CD).

### Step 1: Initialize Git and Commit Your Project
Open PowerShell or Command Prompt in the project folder and run:
```bash
git init
git add .
git commit -m "Initial MindEase full-stack commit for Vercel deployment"
```

### Step 2: Push to a GitHub Repository
1. Go to [github.com/new](https://github.com/new) and create a new repository (e.g., `MindEase-AI`).
2. Link your local project to GitHub and push:
```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### Step 3: Import into Vercel
1. Log in to [vercel.com](https://vercel.com) and click **"Add New..."** ➔ **"Project"**.
2. Under **Import Git Repository**, find your `MindEase-AI` repository and click **Import**.
3. Under **Project Name**, keep `mindease` or choose your custom name.
4. Leave **Framework Preset** as **Other**.
5. Leave **Root Directory** as `./`.

### Step 4: Configure Environment Variables
Under the **Environment Variables** section, add your credentials:
| Key | Value | Description |
| :--- | :--- | :--- |
| `GROQ_API_KEY` | `gsk_...` *(your secret key)* | Required for real-time neural emotion detection & conversational empathy. |
| `GROQ_MODEL` | `openai/gpt-oss-120b` | Default LLM model identifier. |

### Step 5: Click Deploy! 🚀
1. Click the blue **Deploy** button.
2. Vercel will install dependencies from `requirements.txt`, bundle `api/index.py`, and link static assets.
3. Once finished, you will receive a live URL: `https://your-project-name.vercel.app`.

---

## ⚡ Method 2: Deploy Directly via Vercel CLI

If you prefer to deploy directly from your local terminal without Git:

### Step 1: Run Vercel CLI
Run the following in your project folder:
```bash
npx vercel
```

### Step 2: Follow Terminal Prompts
- **Set up and deploy?** Press `y` and Enter.
- **Which scope?** Choose your Vercel account.
- **Link to existing project?** Type `n` and Enter.
- **Project name?** Press Enter (or type `mindease`).
- **In which directory is your code located?** Press Enter (`./`).
- **Want to modify settings?** Type `n` and Enter.

### Step 3: Add the Groq API Key to Vercel
```bash
npx vercel env add GROQ_API_KEY
```
When prompted, paste your Groq key and select **Production**, **Preview**, and **Development**.

### Step 4: Deploy to Production
```bash
npx vercel --prod
```

---

## 🔍 How to Test Your Deployed Vercel App

Once deployed, test your live production deployment:

1. **Open the Web Application**:
   Navigate to `https://your-project.vercel.app` in your browser.
   - You should see the MindEase 2.0 interface.
   - Test by typing: *"I feel happy today"* or *"I am stressed about exams"*.
   - Verify that the Live Emotion Pill and Radar update in real time.

2. **Check the API Health Endpoint**:
   Navigate to:
   ```
   https://your-project.vercel.app/api/health
   ```
   Expected response:
   ```json
   {
     "status": "healthy",
     "app": "MindEase: Emotion-Aware Mental Wellness Companion",
     "version": "2.0.0",
     "model_classes_count": 15,
     "llm_engine": "Groq (openai/gpt-oss-120b)"
   }
   ```

3. **Check Interactive API Documentation (Swagger)**:
   Navigate to:
   ```
   https://your-project.vercel.app/api/docs
   ```

---

## 🛠️ Troubleshooting & Tips

- **404 on API requests?**
  `vercel.json` already includes the rewrite rule mapping `/api/(.*)` to `api/index.py`. The backend also dual-mounts both `/api/chat` and `/chat`, ensuring requests never fail regardless of URL structure.
- **Read-Only Serverless Filesystem**:
  Vercel serverless environments make the root filesystem read-only. The ML model in `backend/app/ml/emotion_classifier.py` is pre-trained and packaged in `models/emotion_classifier.joblib`, and memory fallbacks prevent any filesystem write errors.
- **Bundle Size**:
  `requirements.txt` has been optimized specifically for serverless deployment by separating out heavy desktop-only dependencies like Streamlit.
