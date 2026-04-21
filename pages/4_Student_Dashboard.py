import streamlit as st
import pandas as pd

st.title("📊 Student Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Jobs Viewed", 12)
col2.metric("Jobs Liked", 5)
col3.metric("Avg Match Score", "85%")

data = pd.DataFrame({
    "Category": ["Marketing", "Product", "Design"],
    "Likes": [3, 1, 1]
})

st.subheader("Liked Jobs by Category")
st.bar_chart(data.set_index("Category"))
st.subheader("🧩 My Task Progress")

# Example tasks (you can change later)
tasks = [
    {"task": "Market Research", "startup": "GrowthAI", "status": "Matched"},
    {"task": "UI Fix", "startup": "BrightLabs", "status": "Assigned"},
    {"task": "Data Cleanup", "startup": "FlowTech", "status": "In Progress"},
    {"task": "User Testing", "startup": "Nova Studio", "status": "Completed"},
]
def status_color(status):
    colors = {
        "Liked": "gray",
        "Matched": "blue",
        "Assigned": "green",
        "In Progress": "orange",
        "Completed": "purple"
    }
    return colors.get(status, "black")
    for t in tasks:
    st.markdown(f"""
    <div style="
        background-color:#1e1e1e;
        padding:15px;
        border-radius:12px;
        margin-bottom:10px;
        box-shadow:0px 2px 10px rgba(0,0,0,0.2);
    ">
        <h4 style="margin:0;">{t['task']} — {t['startup']}</h4>
        <p style="color:{status_color(t['status'])}; font-weight:bold;">
            {t['status']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
