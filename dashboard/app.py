# dashboard/app.py

import streamlit as st
import requests

# === Config ===
API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(page_title="AI Self-Healing Agent", layout="wide")
st.title("🚑 AI-Driven Self-Healing Platform (RL + Logs)")

# === Log Input ===
st.subheader("📄 Enter Log Line")
log_line = st.text_input("Paste a log message", "ERROR dfs.DataXceiver: Socket timeout on block transfer")

# === System Metrics Input ===
st.subheader("📊 Simulate System Metrics")
col1, col2, col3, col4 = st.columns(4)
with col1:
    cpu = st.slider("CPU Usage", 0.0, 1.0, 0.8)
with col2:
    mem = st.slider("Memory Usage", 0.0, 1.0, 0.7)
with col3:
    disk = st.slider("Disk I/O", 0.0, 1.0, 0.6)
with col4:
    error_count = st.number_input("Error Count", 0, 20, 3)

# === Prediction Button ===
if st.button("💡 Predict Action"):
    with st.spinner("Contacting RL agent..."):
        payload = {
            "log": log_line,
            "cpu": cpu,
            "mem": mem,
            "disk": disk,
            "error_count": error_count
        }
        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                data = response.json()
                st.success(f"Agent Action: `{data['action_name']}` (ID {data['action_id']})")
            else:
                st.error(f"Error: {response.text}")
        except Exception as e:
            st.error(f"Connection failed: {e}")
