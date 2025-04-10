# 🤖 AI-Driven Self-Healing Infrastructure Agent

> A full-stack intelligent AIOps platform that observes system logs and metrics, learns from failure patterns, and autonomously decides corrective actions in real-time using Reinforcement Learning.

---

## 📌 Overview

This platform leverages a PPO-based Reinforcement Learning agent trained on real-world big data system logs (from HDFS), augmented with system metrics like CPU, memory, and disk usage. The agent learns to recover from infrastructure issues with actions like restarting services, scaling resources, clearing cache, or alerting human operators.

---

## 🧠 Features

- 🧾 Parses and vectorizes logs using `TF-IDF`
- 📊 Combines logs with simulated system metrics
- 🤖 Trained PPO agent (via `stable-baselines3`)
- 🔁 Multi-action decision logic (restart, scale, cache clear, alert)
- ⚙️ FastAPI backend for inference
- 🖥️ Streamlit dashboard for real-time monitoring

---

## 🏗️ Architecture

```plaintext
           ┌────────────────────────────┐
           │     Web Dashboard (UI)     │ ←─ Streamlit
           └────────────▲───────────────┘
                        │
                        │ REST API calls
                        ▼
              ┌────────────────────┐
              │   FastAPI Backend  │ ←─ Serves PPO model
              └──────▲─────▲───────┘
                     │     │
     Inference       │     │  Log Upload / Simulated Metrics
                     ▼     ▼
     ┌────────────────────────────┐
     │  PPO Agent + TF-IDF Model  │ ←─ Trained on LogHub (HDFS)
     └────────────────────────────┘
```

## Quickstart (Local Dev)
1. Clone & Setup
- git clone https://github.com/yourusername/self-healing-agent.git
- cd self-healing-agent
- python -m venv venv
- source venv/bin/activate  # or venv\Scripts\activate on Windows
- pip install -r requirements.txt

2. Start Backend (FastAPI)
- cd backend
- uvicorn main:app --reload

3. Start Frontend (Streamlit)
- cd dashboard
- streamlit run app.py
