import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Dashboard", layout="wide")

st.markdown("""
<style>
    .stApp {
        background: #F7F8FC;
    }

    .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3 {
        color: #111827;
        letter-spacing: -0.5px;
    }

    .subtle-text {
        color: #6B7280;
        font-size: 15px;
        margin-top: -8px;
        margin-bottom: 20px;
    }

    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 8px 24px rgba(17, 24, 39, 0.06);
        border: 1px solid #ECEEF5;
        margin-bottom: 10px;
    }

    .metric-label {
        font-size: 14px;
        color: #6B7280;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 34px;
        font-weight: 800;
        color: #111827;
        line-height: 1;
    }

    .section-title {
        font-size: 28px;
        font-weight: 800;
        color: #111827;
        margin-top: 28px;
        margin-bottom: 16px;
        letter-spacing: -0.7px;
    }

    .chart-card {
        background: white;
        padding: 22px;
        border-radius: 22px;
        box-shadow: 0 8px 24px rgba(17, 24, 39, 0.06);
        border: 1px solid #ECEEF5;
        margin-bottom: 26px;
    }

    .task-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 16px;
        box-shadow: 0 8px 24px rgba(17, 24, 39, 0.05);
        border: 1px solid #ECEEF5;
    }

    .task-title {
        font-size: 21px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 4px;
    }

    .task-company {
        font-size: 14px;
        color: #6B7280;
        margin-bottom: 14px;
    }

    .status-pill {
        display: inline-block;
        padding: 8px 14px;
        border-radius: 999px;
        color: white;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.2px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 📊 Student Dashboard")
st.markdown('<div class="subtle-text">Your activity, matches, and active startup tasks</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Tasks Viewed</div>
        <div class="metric-value">12</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Tasks Liked</div>
        <div class="metric-value">5</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Avg Match Score</div>
        <div class="metric-value">85%</div>
    </div>
    """, unsafe_allow_html=True)

data = pd.DataFrame({
    "Category": ["Marketing", "Product", "Design"],
    "Likes": [3, 1, 1]
})

st.markdown('<div class="section-title">Liked Tasks by Category</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.bar_chart(data.set_index("Category"))
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">🧩 My Task Progress</div>', unsafe_allow_html=True)

tasks = [
    {"task": "Market Research", "startup": "GrowthAI", "status": "Liked"},
    {"task": "Pitch Deck Update", "startup": "BrightLabs", "status": "Matched"},
    {"task": "Data Cleanup", "startup": "FlowTech", "status": "Assigned"},
    {"task": "User Testing", "startup": "Nova Studio", "status": "In Progress"},
    {"task": "Brand Audit", "startup": "SparkStudio", "status": "Completed"},
]

def status_color(status):
    colors = {
        "Liked": "#EF4444",
        "Matched": "#3B82F6",
        "Assigned": "#10B981",
        "In Progress": "#F59E0B",
        "Completed": "#6B7280"
    }
    return colors.get(status, "#111827")

for t in tasks:
    st.markdown(f"""
    <div class="task-card">
        <div class="task-title">{t['task']}</div>
        <div class="task-company">{t['startup']}</div>
        <div class="status-pill" style="background-color: {status_color(t['status'])};">
            {t['status']}
        </div>
    </div>
    """, unsafe_allow_html=True)
