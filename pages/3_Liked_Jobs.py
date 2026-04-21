import streamlit as st

st.set_page_config(page_title="Liked Jobs", page_icon="❤️", layout="wide")

liked_jobs = [
    {
        "title": "Marketing Intern",
        "startup": "GrowthAI",
        "status": "Saved",
        "match": 85,
        "location": "Zurich"
    },
    {
        "title": "Product Intern",
        "startup": "TechFlow",
        "status": "Matched",
        "match": 92,
        "location": "Remote"
    }
]

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #F8FAFF 0%, #F3F5FB 100%);
    }

    .block-container {
        max-width: 1000px;
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
        margin-bottom: 20px;
    }

    .liked-card {
        background: white;
        border: 1px solid #E8ECF4;
        border-radius: 24px;
        padding: 22px;
        box-shadow: 0 10px 28px rgba(17, 24, 39, 0.05);
        margin-bottom: 16px;
    }

    .job-title {
        font-size: 24px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 4px;
    }

    .job-company {
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

    .saved {
        background: #FEE2E2;
        color: #B91C1C;
    }

    .matched {
        background: #DBEAFE;
        color: #1D4ED8;
    }

    .neutral {
        background: #F3F4F6;
        color: #374151;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">❤️ Liked Jobs</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Tasks you saved or matched with, ready to revisit anytime.</div>', unsafe_allow_html=True)

for job in liked_jobs:
    status_class = "matched" if job["status"] == "Matched" else "saved"

    st.markdown(f"""
    <div class="liked-card">
        <div class="job-title">{job['title']}</div>
        <div class="job-company">🏢 {job['startup']}</div>
        <span class="pill {status_class}">{job['status']}</span>
        <span class="pill neutral">📍 {job['location']}</span>
        <span class="pill neutral">🎯 {job['match']}% match</span>
    </div>
    """, unsafe_allow_html=True)
