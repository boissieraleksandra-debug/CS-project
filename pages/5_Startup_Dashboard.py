import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Startup Dashboard", page_icon="🏢", layout="wide")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #F8FAFF 0%, #F3F5FB 100%);
    }

    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .page-title {
        font-size: 40px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 6px;
    }

    .page-subtitle {
        font-size: 16px;
        color: #6B7280;
        margin-bottom: 24px;
    }

    .summary-card {
        background: white;
        border: 1px solid #E8ECF4;
        border-radius: 24px;
        padding: 20px;
        box-shadow: 0 10px 28px rgba(17, 24, 39, 0.05);
        margin-bottom: 10px;
    }

    .summary-label {
        color: #6B7280;
        font-size: 14px;
        margin-bottom: 8px;
    }

    .summary-value {
        color: #111827;
        font-size: 36px;
        font-weight: 800;
        line-height: 1;
    }

    .section-title {
        font-size: 28px;
        font-weight: 800;
        color: #111827;
        margin-top: 28px;
        margin-bottom: 14px;
    }

    .chart-card {
        background: white;
        border: 1px solid #E8ECF4;
        border-radius: 24px;
        padding: 18px;
        box-shadow: 0 10px 28px rgba(17, 24, 39, 0.05);
        margin-bottom: 22px;
    }

    .applicant-card {
        background: white;
        border: 1px solid #E8ECF4;
        border-radius: 22px;
        padding: 20px;
        box-shadow: 0 10px 28px rgba(17, 24, 39, 0.05);
        margin-bottom: 14px;
    }

    .applicant-title {
        font-size: 20px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 4px;
    }

    .applicant-sub {
        font-size: 14px;
        color: #6B7280;
        margin-bottom: 12px;
    }

    .pill {
        display: inline-block;
        padding: 8px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 800;
        margin-right: 8px;
    }

    .blue {
        background: #DBEAFE;
        color: #1D4ED8;
    }

    .green {
        background: #D1FAE5;
        color: #047857;
    }

    .gray {
        background: #F3F4F6;
        color: #374151;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">🏢 Startup Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Track posted roles, applicants, and category demand at a glance.</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="summary-card">
        <div class="summary-label">Open Roles</div>
        <div class="summary-value">4</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="summary-card">
        <div class="summary-label">Applicants</div>
        <div class="summary-value">18</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="summary-card">
        <div class="summary-label">Avg Pay</div>
        <div class="summary-value">CHF 1.6k</div>
    </div>
    """, unsafe_allow_html=True)

data = pd.DataFrame({
    "Job": ["Marketing", "Product", "Design"],
    "Applicants": [8, 6, 4]
})

fig = px.bar(
    data,
    x="Job",
    y="Applicants",
    color="Job",
    text="Applicants",
    color_discrete_sequence=["#6C63FF", "#4F46E5", "#A78BFA"]
)
fig.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    showlegend=False,
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis_title="",
    yaxis_title=""
)
fig.update_traces(marker_line_width=0)

st.markdown('<div class="section-title">Applicants per Job</div>', unsafe_allow_html=True)
st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">Recent Applicants</div>', unsafe_allow_html=True)

applicants = [
    {"name": "Anna Keller", "job": "Marketing Intern", "status": "Reviewed"},
    {"name": "Leo Martin", "job": "Product Intern", "status": "Interview"},
    {"name": "Maya Chen", "job": "Design Assistant", "status": "New"},
]

for a in applicants:
    status_class = "green" if a["status"] == "Interview" else "blue" if a["status"] == "Reviewed" else "gray"

    st.markdown(f"""
    <div class="applicant-card">
        <div class="applicant-title">{a['name']}</div>
        <div class="applicant-sub">Applied for {a['job']}</div>
        <span class="pill {status_class}">{a['status']}</span>
    </div>
    """, unsafe_allow_html=True)

