import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import sklearn

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Digital Burnout Dashboard",
    page_icon="🧠",
    layout="wide"
)


# ==================================================
# LOAD MODEL
# ==================================================

import streamlit as st
import joblib
import traceback

st.write("Starting model load...")

try:
    model = joblib.load("burnout_predictor.pkl")

    st.success("MODEL LOADED")
    st.write(type(model))

except Exception as e:

    st.error("LOAD FAILED")

    st.code(traceback.format_exc())
# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.stApp{
    background-color:#1F1F1F;
}

section[data-testid="stSidebar"]{
    background-color:#171717;
}

.big-title{
    font-size:38px;
    font-weight:700;
    color:white;
}

.sub-title{
    color:#B0B0B0;
    font-size:16px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("🧠 Burnout AI")

    st.caption(f"Sklearn {sklearn.__version__}")
    st.caption(f"Pandas {pd.__version__}")
    st.caption(f"Numpy {np.__version__}")

    st.markdown("---")

    age = st.slider(
        "Age",
        18,
        65,
        30
    )

    occupation = st.selectbox(
        "Occupation",
        [
            "Content Creator",
            "Student",
            "Software Engineer",
            "Designer",
            "Analyst",
            "Freelancer",
            "Manager"
        ]
    )

    work_mode = st.selectbox(
        "Work Mode",
        [
            "Office",
            "Hybrid",
            "Remote"
        ]
    )

    device_usage_type = st.selectbox(
        "Device Usage Type",
        [
            "Entertainment-Centric",
            "Work-Centric",
            "Balanced"
        ]
    )

    st.markdown("---")

    predict_button = st.button(
        "🚀 Analyze Burnout Risk",
        use_container_width=True
    )

# ==================================================
# HEADER
# ==================================================

st.markdown(
    '<div class="big-title">Digital Burnout Early Detection System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Predict burnout risk using digital behavior and wellness indicators.</div>',
    unsafe_allow_html=True
)

st.markdown("---")

# ==================================================
# INPUTS
# ==================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.subheader("📱 Digital Behavior")

    daily_screen_time = st.slider(
        "Daily Screen Time (Hours)",
        0.0, 18.0, 8.0
    )

    social_media_hours = st.slider(
        "Social Media Hours",
        0.0, 12.0, 3.0
    )

    doomscrolling_duration = st.slider(
        "Doomscrolling Duration",
        0.0, 8.0, 1.0
    )

with col2:

    st.subheader("💼 Productivity")

    deep_work_hours = st.slider(
        "Deep Work Hours",
        0.0, 12.0, 3.0
    )

    distraction_frequency = st.slider(
        "Distraction Frequency",
        0, 100, 20
    )

    meeting_hours = st.slider(
        "Meeting Hours",
        0.0, 10.0, 2.0
    )

with col3:

    st.subheader("🧠 Wellness")

    sleep_hours = st.slider(
        "Sleep Hours",
        0.0, 12.0, 7.0
    )

    sleep_quality = st.slider(
        "Sleep Quality",
        1, 10, 7
    )

    physical_activity = st.slider(
        "Physical Activity",
        0, 10, 5
    )

    stress_level = st.slider(
        "Stress Level",
        1, 10, 5
    )

    motivation_level = st.slider(
        "Motivation Level",
        1, 10, 5
    )

# ==================================================
# FEATURE ENGINEERING
# ==================================================

digital_overload_score = (
    daily_screen_time
    + social_media_hours
    + doomscrolling_duration
)

wellness_score = (
    sleep_quality
    + physical_activity
    + motivation_level
    - stress_level
)

focus_efficiency = (
    deep_work_hours
    / (distraction_frequency + 1)
)

# ==================================================
# PREDICTION
# ==================================================

if predict_button:

    input_df = pd.DataFrame({

        "age": [age],

        "daily_screen_time": [daily_screen_time],
        "social_media_hours": [social_media_hours],
        "doomscrolling_duration": [doomscrolling_duration],

        "deep_work_hours": [deep_work_hours],
        "distraction_frequency": [distraction_frequency],
        "meeting_hours": [meeting_hours],

        "sleep_hours": [sleep_hours],
        "sleep_quality": [sleep_quality],

        "physical_activity": [physical_activity],
        "stress_level": [stress_level],
        "motivation_level": [motivation_level],

        "digital_overload_score": [digital_overload_score],
        "wellness_score": [wellness_score],
        "focus_efficiency": [focus_efficiency],

        "occupation": [occupation],
        "work_mode": [work_mode],
        "device_usage_type": [device_usage_type]

    })

    try:

        prediction = float(model.predict(input_df)[0])

    except Exception as e:

        st.error("Prediction failed")
        st.exception(e)
        st.stop()

    st.markdown("---")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Burnout Risk",
        f"{prediction:.1f}/100"
    )

    c2.metric(
        "Digital Overload",
        f"{digital_overload_score:.1f}"
    )

    c3.metric(
        "Focus Efficiency",
        f"{focus_efficiency:.2f}"
    )

    st.progress(min(int(prediction), 100))

    if prediction < 35:

        category = "🟢 LOW RISK"

        recommendation = """
• Maintain current healthy habits

• Keep a consistent sleep schedule

• Continue regular physical activity

• Preserve work-life balance
"""

    elif prediction < 65:

        category = "🟡 MEDIUM RISK"

        recommendation = """
• Reduce unnecessary screen time

• Increase focus sessions

• Schedule regular breaks

• Improve sleep quality
"""

    else:

        category = "🔴 HIGH RISK"

        recommendation = """
• Reduce digital overload

• Limit doomscrolling behavior

• Prioritize sleep recovery

• Increase physical activity

• Consider workload adjustment
"""

    st.subheader(category)

    col_a, col_b = st.columns(2)

    with col_a:

        st.markdown("### 📊 Burnout Indicators")

        indicators = pd.DataFrame({
            "Metric": [
                "Digital Overload",
                "Wellness Score",
                "Focus Efficiency"
            ],
            "Value": [
                round(digital_overload_score, 2),
                round(wellness_score, 2),
                round(focus_efficiency, 2)
            ]
        })

        st.dataframe(
            indicators,
            use_container_width=True
        )

    with col_b:

        st.markdown("### 💡 Recommendations")

        st.info(recommendation)
