import streamlit as st
import pandas as pd

st.title("📊 Student Dashboard")

# Top metrics
col1, col2, col3 = st.columns(3)

col1.metric("Tasks Viewed", 12)
col2.metric("Tasks Liked", 5)
col3.metric("Avg Match Score", "85%")

# Chart
data = pd.DataFrame({
    "Category": ["Marketing", "Product", "Design"],
    "Likes": [3, 1, 1]
})

st.subheader("Liked Tasks by Category")
st.bar_chart(data.set_index("Category"))

# Task progress section
st.subheader("🧩 My Task Progress")

tasks = [
    {"task": "Market Research", "startup": "GrowthAI", "status": "Matched"},
    {"task": "Pitch Deck Update", "startup": "BrightLabs", "status": "Assigned"},
    {"task": "Data Cleanup", "startup": "FlowTech", "status": "In Progress"},
    {"task": "User Testing", "startup": "Nova Studio", "status": "Completed"},
]

def status_color(status):
    colors = {
        "Liked": "#9CA3AF",
        "Matched": "#3B82F6",
        "Assigned": "#10B981",
        "In Progress": "#F59E0B",
        "Completed": "#8B5CF6"
    }
    return colors.get(status, "#111827")

for t in tasks:
    st.markdown(f"""
    <div style="
        background-color: #ffffff;
        padding: 16px;
        border-radius: 14px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #f0f0f0;
    ">
        <div style="font-size: 18px; font-weight: 600; color: #111827;">
            {t['task']}
        </div>
        <div style="font-size: 14px; color: #6B7280; margin-top: 4px;">
            {t['startup']}
        </div>
        <div style="
            display: inline-block;
            margin-top: 10px;
            padding: 6px 12px;
            border-radius: 999px;
            background-color: {status_color(t['status'])};
            color: white;
            font-size: 13px;
            font-weight: 600;
        ">
            {t['status']}
        </div>
    </div>
    """, unsafe_allow_html=True)
