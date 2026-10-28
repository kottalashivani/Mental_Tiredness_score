import streamlit as st

st.set_page_config(page_title="Mental Tiredness Score Calculator", page_icon="🧠")
st.title("🧠 Mental Tiredness Score Calculator")
st.write("Answer a few questions to get a mental tiredness score from 0 (fresh) to 100 (very tired).")

sleep = st.slider("Hours of sleep per night", 0.0, 12.0, 7.0, 0.5)
screen = st.slider("Screen time per day (hours)", 0.0, 16.0, 6.0, 0.5)
workload = st.slider("Workload / study stress (1 = low, 10 = high)", 1, 10, 5)
mood = st.slider("Mood (1 = very low, 10 = very good)", 1, 10, 6)
exercise = st.slider("Physical activity per day (minutes)", 0, 120, 30, 5)
caffeine = st.slider("Cups of tea/coffee per day", 0, 10, 2)


def calculate_score(sleep, screen, workload, mood, exercise, caffeine):
    """Simple rule-based score. Each factor contributes points; higher = more tired."""
    sleep_pts = max(0, 8 - sleep) / 8 * 30          # up to 30
    screen_pts = min(screen, 12) / 12 * 15           # up to 15
    workload_pts = (workload - 1) / 9 * 25           # up to 25
    mood_pts = (10 - mood) / 9 * 20                  # up to 20
    exercise_pts = max(0, 30 - exercise) / 30 * 5    # up to 5
    caffeine_pts = min(caffeine, 6) / 6 * 5          # up to 5
    return round(sleep_pts + screen_pts + workload_pts + mood_pts + exercise_pts + caffeine_pts)


if st.button("Calculate score"):
    score = calculate_score(sleep, screen, workload, mood, exercise, caffeine)
    st.metric("Mental tiredness score", f"{score} / 100")
    st.progress(score / 100)
    if score < 35:
        st.success("Low tiredness. Keep up your healthy routine.")
    elif score < 65:
        st.warning("Moderate tiredness. Try more sleep, breaks and some exercise.")
    else:
        st.error("High tiredness. Rest, reduce workload where you can, and talk to someone you trust if it continues.")

st.caption("For learning purposes only. This is not a medical or diagnostic tool.")
