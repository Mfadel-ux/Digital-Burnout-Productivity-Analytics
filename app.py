import streamlit as st
import pandas as pd
import numpy as np
import joblib

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

model = joblib.load("burnout_predictor.pkl")

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.stApp{
    background-color:#1F1F1F;
    color:white;
}

section[data-testid="stSidebar"]{
    background-color:#171717;
}

.metric-card{
    background:#2A2A2A;
    padding:20px;
    border-radius:16px;
    border:1px solid #3A3A3A;
}

.dashboard-card{
    background:#2A2A2A;
    padding:25px;
    border-radius:16px;
    border:1px solid #3A3A3A;
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

.low-risk{
    color:#22C55E;
    font-weight:bold;
}

.medium-risk{
    color:#FACC15;
    font-weight:bold;
}

.high-risk{
    color:#EF4444;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("🧠 Burnout AI")

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
            "Student",
            "Analyst",
            "Manager",
            "Software Engineer",
            "Designer",
            "Content Creator"
        ]
    )

    work_mode = st.selectbox(
        "Work Mode",
        [
            "Remote",
            "Hybrid",
            "Office"
        ]
    )

    device_usage_type = st.selectbox(
        "Device Usage Type",
        [
            "Balanced",
            "Work-Centric",
            "Entertainment-Centric"
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
    '<div class="sub-title">Monitor burnout risk using digital behavior, productivity, and wellness indicators.</div>',
    unsafe_allow_html=True
)

st.markdown("")

# ==================================================
# INPUT DASHBOARD
# ==================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.subheader("📱 Digital Behavior")

    daily_screen_time = st.slider(
        "Daily Screen Time",
        0.0,18.0,8.0
    )

    social_media_hours = st.slider(
        "Social Media Hours",
        0.0,12.0,3.0
    )

    doomscrolling_duration = st.slider(
        "Doomscrolling Duration",
        0.0,8.0,1.0
    )

    app_switch_frequency = st.slider(
        "App Switch Frequency",
        0,300,50
    )

    notification_count = st.slider(
        "Notification Count",
        0,500,120
    )

with col2:

    st.subheader("💼 Productivity")

    deep_work_hours = st.slider(
        "Deep Work Hours",
        0.0,12.0,3.0
    )

    distraction_frequency = st.slider(
        "Distraction Frequency",
        0,100,20
    )

    focus_sessions = st.slider(
        "Focus Sessions",
        0,20,5
    )

    meeting_hours = st.slider(
        "Meeting Hours",
        0.0,10.0,2.0
    )

    work_satisfaction = st.slider(
        "Work Satisfaction",
        1,10,5
    )

with col3:

    st.subheader("🧠 Wellness")

    sleep_hours = st.slider(
        "Sleep Hours",
        0.0,12.0,7.0
    )

    sleep_quality = st.slider(
        "Sleep Quality",
        1,10,7
    )

    physical_activity = st.slider(
        "Physical Activity",
        0,10,5
    )

    stress_level = st.slider(
        "Stress Level",
        1,10,5
    )

    motivation_level = st.slider(
        "Motivation Level",
        1,10,5
    )

# ==================================================
# FEATURE ENGINEERING
# ==================================================

digital_overload_score = (
    daily_screen_time +
    social_media_hours +
    doomscrolling_duration
)

wellness_score = (
    sleep_quality +
    physical_activity +
    motivation_level -
    stress_level
)

focus_efficiency = (
    deep_work_hours /
    (distraction_frequency + 1)
)

# ==================================================
# PREDICTION
# ==================================================

if predict_button:

    input_df = pd.DataFrame({

        "age":[age],

        "daily_screen_time":[daily_screen_time],
        "social_media_hours":[social_media_hours],
        "doomscrolling_duration":[doomscrolling_duration],

        "app_switch_frequency":[app_switch_frequency],
        "notification_count":[notification_count],

        "focus_sessions":[focus_sessions],
        "deep_work_hours":[deep_work_hours],
        "distraction_frequency":[distraction_frequency],

        "sleep_hours":[sleep_hours],
        "sleep_quality":[sleep_quality],

        "physical_activity":[physical_activity],
        "stress_level":[stress_level],

        "meeting_hours":[meeting_hours],
        "motivation_level":[motivation_level],

        "work_satisfaction":[work_satisfaction],

        "digital_overload_score":[digital_overload_score],
        "wellness_score":[wellness_score],
        "focus_efficiency":[focus_efficiency],

        "occupation":[occupation],
        "work_mode":[work_mode],
        "device_usage_type":[device_usage_type]

    })

    prediction = model.predict(input_df)[0]

    st.markdown("---")

    # ==========================================
    # METRIC CARDS
    # ==========================================

    c1,c2,c3 = st.columns(3)

    c1.metric(
        "Burnout Risk",
        f"{prediction:.1f}"
    )

    c2.metric(
        "Wellness Score",
        f"{wellness_score:.1f}"
    )

    c3.metric(
        "Focus Efficiency",
        f"{focus_efficiency:.2f}"
    )

    st.markdown("### Burnout Risk Level")

    st.progress(
        min(int(prediction),100)
    )

    # ==========================================
    # CATEGORY
    # ==========================================

    if prediction < 35:

        category = "🟢 LOW RISK"

        recommendation = """
        • Maintain current habits
        
        • Continue regular exercise
        
        • Keep healthy sleep schedule
        
        • Preserve work-life balance
        """

    elif prediction < 65:

        category = "🟡 MEDIUM RISK"

        recommendation = """
        • Reduce screen time
        
        • Improve sleep quality
        
        • Schedule recovery breaks
        
        • Increase focus sessions
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

    st.markdown("---")

    colA,colB = st.columns([1,1])

    with colA:

        st.markdown("### 📊 Behavioral Indicators")

        st.write(
            pd.DataFrame({
                "Metric":[
                    "Digital Overload",
                    "Wellness",
                    "Focus Efficiency"
                ],
                "Value":[
                    round(digital_overload_score,2),
                    round(wellness_score,2),
                    round(focus_efficiency,2)
                ]
            })
        )

    with colB:

        st.markdown("### 💡 Recommendations")

        st.info(recommendation)
