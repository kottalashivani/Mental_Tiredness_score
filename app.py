import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

HISTORY_FILE = "history.csv"

st.set_page_config(page_title="Mental Tiredness Score Calculator", page_icon="🧠")
st.title("🧠 Mental Tiredness Score Calculator")
st.write("Track your mental fatigue, get break recommendations and see your trend over time.")


def calculate_score(work_hours, fatigue, cognitive_load):
    """Score from 0 (fresh) to 100 (very tired)."""
    work_pts = np.clip(work_hours / 12, 0, 1) * 30
    fatigue_pts = (fatigue - 1) / 9 * 40
    load_pts = (cognitive_load - 1) / 9 * 30
    return int(round(work_pts + fatigue_pts + load_pts))


def interpret(score):
    if score < 35:
        return "Low", "green", "You're doing well. Take a short 5-minute break every hour to stay fresh."
    if score < 65:
        return "Moderate", "orange", "Take a 15-minute break now: step away from screens, stretch, drink water."
    return "High", "red", "High mental fatigue. Take a longer break (30+ minutes), rest, and reduce your workload today to avoid burnout."


def load_history():
    if os.path.exists(HISTORY_FILE):
        return pd.read_csv(HISTORY_FILE)
    return pd.DataFrame(columns=["time", "work_hours", "fatigue", "cognitive_load", "score"])


work_hours = st.slider("Work hours today", 0.0, 16.0, 8.0, 0.5)
fatigue = st.slider("Self-reported fatigue (1 = fresh, 10 = exhausted)", 1, 10, 5)
cognitive_load = st.slider("Cognitive load (1 = easy tasks, 10 = very demanding)", 1, 10, 5)

if st.button("Calculate and save"):
    score = calculate_score(work_hours, fatigue, cognitive_load)
    level, color, advice = interpret(score)
    st.markdown(f"### Score: **{score} / 100**")
    st.markdown(f"<h3 style='color:{color}'>{level} mental fatigue</h3>", unsafe_allow_html=True)
    st.progress(score / 100)
    st.info(advice)

    history = load_history()
    new_row = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "work_hours": work_hours,
        "fatigue": fatigue,
        "cognitive_load": cognitive_load,
        "score": score,
    }
    history = pd.concat([history, pd.DataFrame([new_row])], ignore_index=True)
    history.to_csv(HISTORY_FILE, index=False)

history = load_history()
if not history.empty:
    st.subheader("Your fatigue trend")
    fig, ax = plt.subplots()
    ax.plot(history["time"], history["score"], marker="o")
    ax.axhline(35, linestyle="--", color="green", alpha=0.5)
    ax.axhline(65, linestyle="--", color="red", alpha=0.5)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Score")
    ax.set_xlabel("Date and time")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig)
    st.subheader("History")
    st.dataframe(history)

st.caption("For learning purposes only. This is not a medical or diagnostic tool.")
