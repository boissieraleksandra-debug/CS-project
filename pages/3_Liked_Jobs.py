import streamlit as st

st.set_page_config(page_title="Liked Jobs", page_icon="❤️", layout="wide")

if "liked_jobs" not in st.session_state:
    st.session_state.liked_jobs = []

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

    .job-description {
        color: #4B5563;
        font-size: 15px;
        line-height: 1.6;
        margin-bottom: 14px;
    }

    .pill {
        display: inline-block;
        padding: 8px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 800;
        margin-right: 8px;
        margin-bottom: 8px;
    }

    .neutral {
        background: #F3F4F6;
        color: #374151;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">❤️ Liked Jobs</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Your saved startup tasks appear here.</div>', unsafe_allow_html=True)

if len(st.session_state.liked_jobs) == 0:
    st.info("You haven’t liked any jobs yet. Go to Discover Jobs and press Like.")
else:
    for i, job in enumerate(st.session_state.liked_jobs):
        st.markdown(f"""
        <div class="liked-card">
            <div class="job-title">{job['title']}</div>
            <div class="job-company">🏢 {job['startup']}</div>
            <div class="job-description">{job['description']}</div>
            <span class="pill neutral">📂 {job['category']}</span>
            <span class="pill neutral">📍 {job['location']}</span>
            <span class="pill neutral">⏳ {job['duration']}</span>
            <span class="pill neutral">💰 {job['pay']}</span>
            <span class="pill neutral">🎯 {job['match']}% match</span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Remove", key=f"remove_{i}"):
            st.session_state.liked_jobs.pop(i)
            st.rerun()

