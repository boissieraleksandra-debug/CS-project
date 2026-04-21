import streamlit as st

st.set_page_config(page_title="Discover Jobs", page_icon="🔍", layout="wide")

if "liked_jobs" not in st.session_state:
    st.session_state.liked_jobs = []

if "applied_jobs" not in st.session_state:
    st.session_state.applied_jobs = []

jobs = [
    {
        "title": "Marketing Intern",
        "startup": "GrowthAI",
        "category": "Marketing",
        "location": "Zurich",
        "duration": "3 months",
        "pay": "CHF 1,500",
        "description": "Help us grow our brand, support social media campaigns, and create lightweight content ideas.",
        "match": 85
    },
    {
        "title": "Product Intern",
        "startup": "TechFlow",
        "category": "Product",
        "location": "Remote",
        "duration": "6 months",
        "pay": "CHF 2,000",
        "description": "Support feature planning, improve user flows, and help collect user feedback for product decisions.",
        "match": 92
    },
    {
        "title": "Design Assistant",
        "startup": "CreativeLab",
        "category": "Design",
        "location": "Geneva",
        "duration": "2 months",
        "pay": "CHF 1,200",
        "description": "Assist the design team with UI screens, branding assets, and clean presentation materials.",
        "match": 78
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
        letter-spacing: -0.6px;
    }

    .page-subtitle {
        font-size: 16px;
        color: #6B7280;
        margin-bottom: 22px;
    }

    .job-card {
        background: white;
        border: 1px solid #E8ECF4;
        border-radius: 28px;
        padding: 24px;
        box-shadow: 0 16px 40px rgba(17, 24, 39, 0.06);
        margin-bottom: 22px;
    }

    .top-row {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 16px;
    }

    .job-title {
        font-size: 28px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 4px;
        letter-spacing: -0.6px;
    }

    .job-startup {
        font-size: 15px;
        color: #6B7280;
        margin-bottom: 12px;
    }

    .match-pill {
        background: #EEF2FF;
        color: #4338CA;
        padding: 10px 14px;
        border-radius: 999px;
        font-size: 13px;
        font-weight: 800;
        white-space: nowrap;
    }

    .meta-row {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 14px;
    }

    .meta-pill {
        background: #F3F4F6;
        color: #374151;
        padding: 8px 12px;
        border-radius: 999px;
        font-size: 13px;
        font-weight: 700;
    }

    .job-description {
        color: #4B5563;
        font-size: 15px;
        line-height: 1.7;
        margin-bottom: 18px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">🔍 Discover Jobs</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Browse startup tasks and save the ones you like.</div>', unsafe_allow_html=True)

for i, job in enumerate(jobs):
    st.markdown(f"""
    <div class="job-card">
        <div class="top-row">
            <div>
                <div class="job-title">{job['title']}</div>
                <div class="job-startup">🏢 {job['startup']}</div>
            </div>
            <div class="match-pill">🎯 {job['match']}% match</div>
        </div>

        <div class="meta-row">
            <div class="meta-pill">📂 {job['category']}</div>
            <div class="meta-pill">📍 {job['location']}</div>
            <div class="meta-pill">⏳ {job['duration']}</div>
            <div class="meta-pill">💰 {job['pay']}</div>
        </div>

        <div class="job-description">{job['description']}</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.button("❌ Pass", key=f"pass_{i}", use_container_width=True)

    with col2:
        st.button("👀 Details", key=f"details_{i}", use_container_width=True)

    with col3:
        if st.button("❤️ Like", key=f"like_{i}", use_container_width=True):
            already_liked = any(
                liked_job["title"] == job["title"] and liked_job["startup"] == job["startup"]
                for liked_job in st.session_state.liked_jobs
            )

            already_applied = any(
                applied_job["title"] == job["title"] and applied_job["startup"] == job["startup"]
                for applied_job in st.session_state.applied_jobs
            )

            if already_applied:
                st.info(f"You already applied to {job['title']} at {job['startup']}.")
            elif not already_liked:
                st.session_state.liked_jobs.append(job)
                st.success(f"You liked {job['title']} at {job['startup']}.")
            else:
                st.info(f"{job['title']} is already in your liked jobs.")
             
