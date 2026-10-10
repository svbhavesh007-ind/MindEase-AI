/**
 * MindEase 2.0 Frontend Controller
 * Handles Emotion Analytics, Empathetic Chat, 4-7-8 Breathing, Voice Audio, & Safety Triage
 */

document.addEventListener("DOMContentLoaded", () => {
  // Initialize Feather Icons
  if (window.feather) {
    feather.replace();
  }

  // State Management
  const state = {
    history: [],
    sessionStats: {
      messageCount: 0,
      dominantEmotion: "Neutral",
      exerciseCount: 0,
      emotionFrequencies: {}
    },
    voiceEnabled: true,
    isListening: false,
    breathingTimer: null,
    breathingPhase: "ready", // ready, inhale, hold, exhale
    breathingCountdown: 4,
    breathingCycles: 0,
    journalEntries: JSON.parse(localStorage.getItem("mindease_journal") || "[]")
  };

  // DOM Elements
  const chatMessages = document.getElementById("chat-messages");
  const chatForm = document.getElementById("chat-form");
  const userInput = document.getElementById("user-input");
  const typingIndicator = document.getElementById("typing-indicator");
  const welcomeBanner = document.getElementById("welcome-banner");
  
  // Navigation & Theme
  const btnToggleTheme = document.getElementById("btn-toggle-theme");
  const iconTheme = document.getElementById("icon-theme");
  const btnToggleVoice = document.getElementById("btn-toggle-voice");
  const btnOpenWellness = document.getElementById("btn-open-wellness");
  const btnCloseDrawer = document.getElementById("btn-close-drawer");
  const wellnessDrawer = document.getElementById("wellness-drawer");
  const btnSos = document.getElementById("btn-sos");
  const crisisModal = document.getElementById("crisis-modal");
  const btnCloseModal = document.getElementById("btn-close-modal");
  const btnDismissCrisis = document.getElementById("btn-dismiss-crisis");
  const btnMic = document.getElementById("btn-mic");
  const btnClearChat = document.getElementById("btn-clear-chat");

  // Emotion Left Panel
  const detectedEmotionName = document.getElementById("detected-emotion-name");
  const detectedEmotionTheme = document.getElementById("detected-emotion-theme");
  const emotionAvatar = document.getElementById("emotion-avatar");
  const valenceVal = document.getElementById("valence-val");
  const valenceFill = document.getElementById("valence-fill");
  const emotionCardGlow = document.getElementById("emotion-card-glow");
  const probabilityBars = document.getElementById("probability-bars");
  const globalEmotionEmoji = document.getElementById("global-emotion-emoji");
  const globalEmotionText = document.getElementById("global-emotion-text");
  const globalConfidenceTag = document.getElementById("global-confidence-tag");

  // Stats
  const statMessages = document.getElementById("stat-messages");
  const statPrimaryMood = document.getElementById("stat-primary-mood");
  const statExercises = document.getElementById("stat-exercises");

  // Wellness Elements
  const tabButtons = document.querySelectorAll(".wellness-tabs .tab-btn");
  const tabContents = document.querySelectorAll(".tab-content");
  const btnStartBreathing = document.getElementById("btn-start-breathing");
  const btnStopBreathing = document.getElementById("btn-stop-breathing");
  const breathingBubble = document.getElementById("breathing-bubble");
  const breathingPhaseText = document.getElementById("breathing-phase");
  const breathingTimerText = document.getElementById("breathing-timer");
  const breathingCyclesText = document.getElementById("breathing-cycles");
  const btnQuickStart = document.getElementById("btn-quick-start");
  const btnWelcomeBreathing = document.getElementById("btn-welcome-breathing");

  // Journal Elements
  const journalForm = document.getElementById("journal-form");
  const journalTitle = document.getElementById("journal-title");
  const journalContent = document.getElementById("journal-content");
  const journalEntriesList = document.getElementById("journal-entries-list");
  const btnCompleteGrounding = document.getElementById("btn-complete-grounding");

  // Audio Chime
  const audioChime = document.getElementById("audio-chime");

  // =========================================================================
  // Theme Toggle & Persistence
  // =========================================================================
  const savedTheme = localStorage.getItem("mindease_theme") || "dark";
  document.documentElement.setAttribute("data-theme", savedTheme);
  updateThemeIcon(savedTheme);

  btnToggleTheme.addEventListener("click", () => {
    const currentTheme = document.documentElement.getAttribute("data-theme");
    const nextTheme = currentTheme === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", nextTheme);
    localStorage.setItem("mindease_theme", nextTheme);
    updateThemeIcon(nextTheme);
  });

  function updateThemeIcon(theme) {
    if (iconTheme) {
      iconTheme.setAttribute("data-feather", theme === "dark" ? "sun" : "moon");
      if (window.feather) feather.replace();
    }
  }

  // =========================================================================
  // Wellness Drawer & Modal Toggles
  // =========================================================================
  btnOpenWellness.addEventListener("click", () => {
    wellnessDrawer.classList.toggle("open");
  });

  btnCloseDrawer.addEventListener("click", () => {
    wellnessDrawer.classList.remove("open");
  });

  btnSos.addEventListener("click", () => {
    crisisModal.classList.add("open");
  });

  btnCloseModal.addEventListener("click", () => {
    crisisModal.classList.remove("open");
  });

  btnDismissCrisis.addEventListener("click", () => {
    crisisModal.classList.remove("open");
  });

  // Mobile Sidebar (Mood Radar Drawer)
  const btnToggleSidebar = document.getElementById("btn-toggle-sidebar");
  const btnCloseSidebar = document.getElementById("btn-close-sidebar");
  const sidebarLeft = document.getElementById("sidebar-left");
  const sidebarBackdrop = document.getElementById("sidebar-backdrop");

  if (btnToggleSidebar) {
    btnToggleSidebar.addEventListener("click", () => {
      sidebarLeft.classList.toggle("open");
      if (sidebarBackdrop) sidebarBackdrop.classList.toggle("open");
    });
  }
  if (btnCloseSidebar) {
    btnCloseSidebar.addEventListener("click", () => {
      sidebarLeft.classList.remove("open");
      if (sidebarBackdrop) sidebarBackdrop.classList.remove("open");
    });
  }
  if (sidebarBackdrop) {
    sidebarBackdrop.addEventListener("click", () => {
      sidebarLeft.classList.remove("open");
      sidebarBackdrop.classList.remove("open");
    });
  }

  // Tab switching
  tabButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      const tabId = btn.getAttribute("data-tab");
      tabButtons.forEach(b => b.classList.remove("active"));
      tabContents.forEach(c => c.classList.remove("active"));
      btn.classList.add("active");
      const targetContent = document.getElementById(`tab-${tabId}`);
      if (targetContent) targetContent.classList.add("active");
    });
  });

  btnQuickStart.addEventListener("click", () => {
    userInput.focus();
    welcomeBanner.style.display = "none";
  });

  btnWelcomeBreathing.addEventListener("click", () => {
    wellnessDrawer.classList.add("open");
    tabButtons[0].click(); // Activate breathing tab
  });

  // =========================================================================
  // Voice Synthesis (TTS) & Recognition (STT)
  // =========================================================================
  btnToggleVoice.addEventListener("click", () => {
    state.voiceEnabled = !state.voiceEnabled;
    const btnText = btnToggleVoice.querySelector(".btn-text");
    const icon = btnToggleVoice.querySelector("i");
    if (state.voiceEnabled) {
      btnText.textContent = "Voice: ON";
      icon.setAttribute("data-feather", "volume-2");
    } else {
      btnText.textContent = "Voice: OFF";
      icon.setAttribute("data-feather", "volume-x");
      window.speechSynthesis.cancel();
    }
    if (window.feather) feather.replace();
  });

  function speakText(text) {
    if (!state.voiceEnabled || !window.speechSynthesis) return;
    window.speechSynthesis.cancel();

    // Clean markdown symbols for natural speech
    const cleanSpeech = text
      .replace(/[*_#`~[\]]/g, "")
      .replace(/https?:\/\/\S+/g, "")
      .replace(/tel:\S+/g, "");

    const utterance = new SpeechSynthesisUtterance(cleanSpeech);
    utterance.rate = 0.95; // Gentle pacing
    utterance.pitch = 1.05;

    // Pick soothing English voice if available
    const voices = window.speechSynthesis.getVoices();
    const gentleVoice = voices.find(v => v.lang.startsWith("en") && (v.name.includes("Natural") || v.name.includes("Samantha") || v.name.includes("Google") || v.name.includes("Karen")));
    if (gentleVoice) utterance.voice = gentleVoice;

    window.speechSynthesis.speak(utterance);
  }

  // Speech Recognition (Mic Input)
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  let recognition = null;
  if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-US";

    recognition.onstart = () => {
      state.isListening = true;
      btnMic.classList.add("listening");
      userInput.placeholder = "Listening to your voice... Speak freely";
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      userInput.value = transcript;
      userInput.focus();
    };

    recognition.onerror = () => {
      state.isListening = false;
      btnMic.classList.remove("listening");
      userInput.placeholder = "How are you feeling right now? Share anything on your mind...";
    };

    recognition.onend = () => {
      state.isListening = false;
      btnMic.classList.remove("listening");
      userInput.placeholder = "How are you feeling right now? Share anything on your mind...";
    };

    btnMic.addEventListener("click", () => {
      if (state.isListening) {
        recognition.stop();
      } else {
        recognition.start();
      }
    });
  } else {
    btnMic.style.display = "none"; // Hide if unsupported
  }

  // =========================================================================
  // Quick Feeling Chips
  // =========================================================================
  document.querySelectorAll(".chip").forEach(chip => {
    chip.addEventListener("click", () => {
      const promptText = chip.getAttribute("data-prompt");
      userInput.value = promptText;
      sendMessage(promptText);
    });
  });

  // Auto-resize textarea
  userInput.addEventListener("input", () => {
    userInput.style.height = "auto";
    userInput.style.height = Math.min(userInput.scrollHeight, 140) + "px";
  });

  userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      chatForm.dispatchEvent(new Event("submit"));
    }
  });

  // Clear Chat Session
  btnClearChat.addEventListener("click", () => {
    if (confirm("Reset current conversation session?")) {
      chatMessages.innerHTML = "";
      state.history = [];
      welcomeBanner.style.display = "block";
      updateEmotionDashboard({
        primary_emotion: "neutral",
        confidence: 0.5,
        confidence_percentage: "50%",
        emoji: "🌿",
        valence: "neutral",
        actionable_theme: "Ready for open dialogue",
        breakdown: [
          { emotion: "neutral", percentage: 50 },
          { emotion: "calm", percentage: 30 },
          { emotion: "hope", percentage: 20 }
        ]
      });
    }
  });

  // =========================================================================
  // Chat Submission & Real-Time Emotion Processing
  // =========================================================================
  chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const text = userInput.value.trim();
    if (!text) return;
    sendMessage(text);
  });

  async function sendMessage(text) {
    // Hide welcome banner on first message
    welcomeBanner.style.display = "none";

    // 1. Render User Message
    renderMessage("user", text);
    userInput.value = "";
    userInput.style.height = "auto";
    state.history.push({ role: "user", content: text });

    // Update message stats
    state.sessionStats.messageCount++;
    statMessages.textContent = state.sessionStats.messageCount;

    // Show Typing Indicator & Scroll
    typingIndicator.style.display = "flex";
    scrollToBottom();

    if (window.location.protocol === "file:") {
      typingIndicator.style.display = "none";
      renderMessage(
        "assistant",
        "⚠️ **Backend is not connected!** You opened this file directly from your file manager (`file:///`).\n\n• **For Local Use:** Double-click `run.bat` and visit `http://127.0.0.1:8000`.\n• **For Vercel:** Open your live deployment URL (`https://your-project.vercel.app`)."
      );
      scrollToBottom();
      return;
    }

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: text,
          history: state.history.slice(-6)
        })
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Server returned status ${response.status}: ${errorText}`);
      }

      const data = await response.json();
      typingIndicator.style.display = "none";

      // 2. Render Assistant Message with Emotion Pill and Exercise
      renderMessage("assistant", data.reply, data.emotion, data.recommended_exercise);
      state.history.push({ role: "assistant", content: data.reply });

      // 3. Update Emotional Intelligence Dashboard
      updateEmotionDashboard(data.emotion);

      // 4. Crisis Intervention Trigger
      if (data.crisis && data.crisis.is_crisis) {
        crisisModal.classList.add("open");
      }

      // 5. Speak response aloud if enabled
      speakText(data.reply);

    } catch (err) {
      console.error("Chat communication error:", err);
      typingIndicator.style.display = "none";
      const errDetail = err && err.message ? err.message : String(err);
      renderMessage(
        "assistant",
        `I'm listening and I want to support you, though I encountered an issue connecting to the backend server.\n\n🔍 **Diagnostics:** \`${errDetail}\`\n\n• **If running locally:** Ensure \`run.bat\` is running (server on \`http://127.0.0.1:8000\`).\n• **If on Vercel:** Check that \`GROQ_API_KEY\` is added in Project Settings ➔ Environment Variables, and verify your Vercel deployment status.`
      );
    }

    scrollToBottom();
  }

  // =========================================================================
  // Render Chat Message Bubbles
  // =========================================================================
  function renderMessage(role, text, emotion = null, exercise = null) {
    const row = document.createElement("div");
    row.className = `message-row ${role}`;

    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const isUser = role === "user";

    // Format markdown-like bold text & linebreaks
    const formattedText = escapeHtml(text)
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\n\n/g, '<br><br>')
      .replace(/\n/g, '<br>');

    let emotionBadgeHtml = "";
    if (emotion && !isUser) {
      const valenceClass = (emotion.valence || "neutral").toLowerCase();
      emotionBadgeHtml = `
        <div class="message-emotion-badge emotion-${valenceClass}">
          <span class="badge-emoji">${emotion.emoji}</span>
          <div class="badge-details">
            <span class="badge-emotion">${emotion.primary_emotion.toUpperCase()}</span>
            <span class="badge-meta">${emotion.confidence_percentage} &bull; ${escapeHtml(emotion.actionable_theme || "Attuned")}</span>
          </div>
        </div>
      `;
    }

    let exerciseHtml = "";
    if (exercise && !isUser) {
      exerciseHtml = `
        <div class="exercise-suggestion-card">
          <div class="exercise-suggestion-meta">
            <h5><i data-feather="feather"></i> Recommended: ${escapeHtml(exercise.title)}</h5>
            <p>${escapeHtml(exercise.description)}</p>
          </div>
          <button class="btn-exercise-launch" data-exercise-id="${exercise.id}">
            Start Exercise
          </button>
        </div>
      `;
    }

    const actionsHtml = !isUser ? `
      <div class="message-actions">
        <button class="msg-action-btn btn-read-aloud" title="Listen to this reply">
          <i data-feather="volume-2"></i> Listen
        </button>
        <button class="msg-action-btn btn-copy-msg" title="Copy text">
          <i data-feather="copy"></i> Copy
        </button>
      </div>
    ` : "";

    row.innerHTML = `
      <div class="message-avatar">
        ${isUser ? '👤' : (emotion ? emotion.emoji : '🌱')}
      </div>
      <div class="message-bubble">
        <div class="message-header">
          <span class="message-sender">${isUser ? 'You' : 'MindEase'}</span>
          <span class="message-time">${timeStr}</span>
        </div>
        ${emotionBadgeHtml}
        <div class="message-body">
          ${formattedText}
          ${exerciseHtml}
        </div>
        ${actionsHtml}
      </div>
    `;

    // Attach Listen and Copy action events
    if (!isUser) {
      const readBtn = row.querySelector(".btn-read-aloud");
      if (readBtn) {
        readBtn.addEventListener("click", () => speakText(text));
      }
      const copyBtn = row.querySelector(".btn-copy-msg");
      if (copyBtn) {
        copyBtn.addEventListener("click", () => {
          navigator.clipboard.writeText(text);
          copyBtn.innerHTML = `<i data-feather="check"></i> Copied!`;
          if (window.feather) feather.replace();
          setTimeout(() => {
            copyBtn.innerHTML = `<i data-feather="copy"></i> Copy`;
            if (window.feather) feather.replace();
          }, 2000);
        });
      }
      const launchBtn = row.querySelector(".btn-exercise-launch");
      if (launchBtn) {
        launchBtn.addEventListener("click", () => {
          wellnessDrawer.classList.add("open");
          const exId = launchBtn.getAttribute("data-exercise-id");
          if (exId === "breathing_478") tabButtons[0].click();
          else if (exId === "grounding_54321") tabButtons[1].click();
          else tabButtons[2].click();
        });
      }
    }

    chatMessages.appendChild(row);
    if (window.feather) feather.replace();
  }

  function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function escapeHtml(string) {
    const div = document.createElement('div');
    div.innerText = string;
    return div.innerHTML;
  }

  // =========================================================================
  // Update Emotional Intelligence Dashboard
  // =========================================================================
  function updateEmotionDashboard(emotion) {
    if (!emotion) return;

    // Card Update
    detectedEmotionName.textContent = `${emotion.primary_emotion}`;
    detectedEmotionTheme.textContent = emotion.actionable_theme;
    emotionAvatar.textContent = emotion.emoji;

    // Valence progress
    valenceVal.textContent = emotion.valence;
    valenceVal.className = `valence-val ${emotion.valence}`;
    if (emotion.valence === "positive") {
      valenceFill.style.width = "85%";
      valenceFill.style.background = "linear-gradient(90deg, #10b981, #14b8a6)";
      emotionCardGlow.style.background = "#10b981";
    } else if (emotion.valence === "negative") {
      valenceFill.style.width = "25%";
      valenceFill.style.background = "linear-gradient(90deg, #ef4444, #f59e0b)";
      emotionCardGlow.style.background = "#f59e0b";
    } else {
      valenceFill.style.width = "50%";
      valenceFill.style.background = "linear-gradient(90deg, #6366f1, #14b8a6)";
      emotionCardGlow.style.background = "#6366f1";
    }

    // Nav status pill
    globalEmotionEmoji.textContent = emotion.emoji;
    globalEmotionText.textContent = `Active: ${emotion.primary_emotion.toUpperCase()}`;
    globalConfidenceTag.textContent = emotion.confidence_percentage;

    // Probability Bars breakdown
    if (emotion.breakdown && emotion.breakdown.length > 0) {
      probabilityBars.innerHTML = "";
      emotion.breakdown.slice(0, 4).forEach(item => {
        const row = document.createElement("div");
        row.className = "prob-row";
        row.innerHTML = `
          <span class="prob-name">${item.emotion}</span>
          <div class="prob-track">
            <div class="prob-fill" style="width: ${item.percentage}%; background: var(--accent);"></div>
          </div>
          <span class="prob-percent">${item.percentage}%</span>
        `;
        probabilityBars.appendChild(row);
      });
    }

    // Update Dominant mood stat
    state.sessionStats.emotionFrequencies[emotion.primary_emotion] = 
      (state.sessionStats.emotionFrequencies[emotion.primary_emotion] || 0) + 1;
    
    let maxEmotion = "Neutral";
    let maxCount = 0;
    for (const [emo, count] of Object.entries(state.sessionStats.emotionFrequencies)) {
      if (count > maxCount) {
        maxCount = count;
        maxEmotion = emo;
      }
    }
    statPrimaryMood.textContent = maxEmotion.charAt(0).toUpperCase() + maxEmotion.slice(1);
  }

  // =========================================================================
  // Interactive 4-7-8 Breathing Technique
  // =========================================================================
  btnStartBreathing.addEventListener("click", startBreathingCycle);
  btnStopBreathing.addEventListener("click", stopBreathingCycle);

  function startBreathingCycle() {
    btnStartBreathing.disabled = true;
    btnStopBreathing.disabled = false;
    state.breathingCycles = 0;
    runInhalePhase();
  }

  function stopBreathingCycle() {
    clearInterval(state.breathingTimer);
    btnStartBreathing.disabled = false;
    btnStopBreathing.disabled = true;
    breathingBubble.className = "breathing-circle-core";
    breathingPhaseText.textContent = "Ready";
    breathingTimerText.textContent = "4s";
  }

  function playChime() {
    try {
      if (audioChime) {
        audioChime.currentTime = 0;
        audioChime.volume = 0.3;
        audioChime.play().catch(() => {});
      }
    } catch (e) {}
  }

  function runInhalePhase() {
    state.breathingPhase = "inhale";
    breathingBubble.className = "breathing-circle-core inhale";
    breathingPhaseText.textContent = "Inhale...";
    let count = 4;
    breathingTimerText.textContent = `${count}s`;
    playChime();

    state.breathingTimer = setInterval(() => {
      count--;
      if (count > 0) {
        breathingTimerText.textContent = `${count}s`;
      } else {
        clearInterval(state.breathingTimer);
        runHoldPhase();
      }
    }, 1000);
  }

  function runHoldPhase() {
    state.breathingPhase = "hold";
    breathingBubble.className = "breathing-circle-core hold";
    breathingPhaseText.textContent = "Hold Gently...";
    let count = 7;
    breathingTimerText.textContent = `${count}s`;

    state.breathingTimer = setInterval(() => {
      count--;
      if (count > 0) {
        breathingTimerText.textContent = `${count}s`;
      } else {
        clearInterval(state.breathingTimer);
        runExhalePhase();
      }
    }, 1000);
  }

  function runExhalePhase() {
    state.breathingPhase = "exhale";
    breathingBubble.className = "breathing-circle-core exhale";
    breathingPhaseText.textContent = "Release & Exhale...";
    let count = 8;
    breathingTimerText.textContent = `${count}s`;

    state.breathingTimer = setInterval(() => {
      count--;
      if (count > 0) {
        breathingTimerText.textContent = `${count}s`;
      } else {
        clearInterval(state.breathingTimer);
        state.breathingCycles++;
        breathingCyclesText.textContent = `Cycles completed: ${state.breathingCycles} / 4`;
        
        state.sessionStats.exerciseCount++;
        statExercises.textContent = state.sessionStats.exerciseCount;

        if (state.breathingCycles < 4) {
          runInhalePhase();
        } else {
          stopBreathingCycle();
          breathingPhaseText.textContent = "Complete!";
          breathingTimerText.textContent = "Namaste ✨";
        }
      }
    }, 1000);
  }

  // =========================================================================
  // 5-4-3-2-1 Grounding Completion
  // =========================================================================
  btnCompleteGrounding.addEventListener("click", () => {
    state.sessionStats.exerciseCount++;
    statExercises.textContent = state.sessionStats.exerciseCount;
    btnCompleteGrounding.innerHTML = `<i data-feather="check"></i> Grounding Anchors Saved!`;
    if (window.feather) feather.replace();
    setTimeout(() => {
      btnCompleteGrounding.innerHTML = `<i data-feather="check-circle"></i> Save Grounding Anchor`;
      if (window.feather) feather.replace();
      wellnessDrawer.classList.remove("open");
    }, 1500);
  });

  // =========================================================================
  // Mood Journaling
  // =========================================================================
  renderJournalEntries();

  journalForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const title = journalTitle.value.trim();
    const content = journalContent.value.trim();
    if (!content) return;

    try {
      const res = await fetch("/api/journal", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, content })
      });
      const data = await res.json();
      
      const newEntry = {
        id: Date.now().toString(),
        title: title || "Daily Reflection",
        content,
        timestamp: new Date().toLocaleDateString() + " " + new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        emotion: data.emotion,
        ai_reflection: data.ai_reflection
      };

      state.journalEntries.unshift(newEntry);
      localStorage.setItem("mindease_journal", JSON.stringify(state.journalEntries));
      
      journalTitle.value = "";
      journalContent.value = "";
      renderJournalEntries();
    } catch (err) {
      console.error("Error saving journal entry:", err);
    }
  });

  function renderJournalEntries() {
    journalEntriesList.innerHTML = "";
    if (state.journalEntries.length === 0) {
      journalEntriesList.innerHTML = `<p style="font-size: 0.78rem; color: var(--text-muted); text-align: center;">No reflections yet. Write your thoughts above to begin.</p>`;
      return;
    }

    state.journalEntries.slice(0, 5).forEach(entry => {
      const card = document.createElement("div");
      card.className = "journal-entry-card";
      card.innerHTML = `
        <div class="entry-header">
          <strong>${escapeHtml(entry.title)}</strong>
          <span>${entry.timestamp}</span>
        </div>
        <p style="color: var(--text-secondary); margin-bottom: 6px;">${escapeHtml(entry.content)}</p>
        ${entry.emotion ? `<span class="message-emotion-pill">${entry.emotion.emoji} ${entry.emotion.primary_emotion.toUpperCase()}</span>` : ''}
        ${entry.ai_reflection ? `<div class="entry-reflection">${escapeHtml(entry.ai_reflection)}</div>` : ''}
      `;
      journalEntriesList.appendChild(card);
    });
  }

});
