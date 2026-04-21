import streamlit as st
import pandas as pd

st.title("📊 Student Dashboard")
st.caption("Your activity, matches, and active startup tasks")

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Tasks Viewed", 12)
col2.metric("Tasks Liked", 5)
col3.metric("Avg Match Score", "85%")

# Chart
data = pd.DataFrame({
    "Category": ["Marketing", "Product", "Design"],
    "Likes": [3, 1, 1]
})

st.markdown("### Liked Tasks by Category")
st.bar_chart(data.set_index("Category"))

# Task progress
st.markdown("### 🧩 My Task Progress")

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
    <div style="
        background-color: #FFFFFF;
        padding: 18px;
        border-radius: 18px;
        margin-bottom: 14px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
        border: 1px solid #ECEEF5;
    ">
        <div style="font-size: 18px; font-weight: 700; color: #111827;">
            {t['task']}
        </div>
        <div style="font-size: 14px; color: #6B7280; margin-top: 4px;">
            {t['startup']}
        </div>
        <div style="
            display: inline-block;
            margin-top: 12px;
            padding: 7px 14px;
            border-radius: 999px;
            background-color: {status_color(t['status'])};
            color: white;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.2px;
        ">
            {t['status']}
        </div>
    </div>
    """, unsafe_allow_html=True)
