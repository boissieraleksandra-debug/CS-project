import streamlit as st

st.set_page_config(
    page_title="SkillSwipe",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* Main app background */
.stApp {
    background-color: #F7F8FC;
}

/* Page padding */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* Headings */
h1, h2, h3 {
    color: #111827;
    font-family: "Arial", sans-serif;
}

/* Card style */
.card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.06);
    border: 1px solid #ECEEF5;
    margin-bottom: 16px;
}

/* Small badge */
.badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
    color: white;
}

/* Subtitle */
.subtitle {
    color: #6B7280;
    font-size: 16px;
    margin-top: -8px;
    margin-bottom: 18px;
}

/* Section spacing */
.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #111827;
    margin-top: 30px;
    margin-bottom: 12px;
}

/* Make metrics cleaner */
[data-testid="stMetric"] {
    background: white;
    border: 1px solid #ECEEF5;
    padding: 16px;
    border-radius: 18px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🚀 SkillSwipe</h1>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Match students with startups for flexible, short-term tasks.</div>",
    unsafe_allow_html=True
)

st.markdown("""
<div class="card">
    <h3>Welcome</h3>
    <p>
        SkillSwipe helps students discover startup micro-tasks that match their skills,
        interests, and availability.
    </p>
    <p>
        Use the sidebar to explore your profile, discover tasks, track your progress,
        and view dashboards.
    </p>
</div>
""", unsafe_allow_html=True)
