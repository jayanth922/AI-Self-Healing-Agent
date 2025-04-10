# backend/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
from stable_baselines3 import PPO

# === Load Model + TF-IDF ===
model = PPO.load("../model/ppo_self_healing_agent.zip")
tfidf = joblib.load("../model/tfidf_vectorizer.pkl")

app = FastAPI(title="Self-Healing RL Agent API")

# === Pydantic Schemas ===
class PredictRequest(BaseModel):
    log: str
    cpu: float
    mem: float
    disk: float
    error_count: int

class PredictResponse(BaseModel):
    action_id: int
    action_name: str

# === Action Map ===
ACTION_MAP = {
    0: "⏸️ Do nothing",
    1: "🔁 Restart",
    2: "📈 Scale up",
    3: "🧹 Clear cache",
    4: "📣 Alert human"
}

# === Predict Endpoint ===
@app.post("/predict", response_model=PredictResponse)
def predict_action(req: PredictRequest):
    try:
        # Encode the log
        log_vector = tfidf.transform([req.log]).toarray()

        # Combine into one observation
        obs = np.concatenate([
            log_vector[0],
            [req.cpu, req.mem, req.disk, req.error_count]
        ]).reshape(1, -1)

        # Inference
        action, _ = model.predict(obs, deterministic=True)

        return PredictResponse(
            action_id=int(action),
            action_name=ACTION_MAP[int(action)]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# === Health Check ===
@app.get("/model/status")
def model_status():
    return {
        "status": "✅ model loaded",
        "vectorizer_dim": len(tfidf.get_feature_names_out()),
        "actions_supported": ACTION_MAP
    }
