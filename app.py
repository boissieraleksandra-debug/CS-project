import streamlit as st

st.set_page_config(
    page_title="SkillSwipe",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #F8FAFF 0%, #F3F5FB 100%);
    }

    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    h1, h2, h3 {
        color: #111827;
        letter-spacing: -0.4px;
    }

    p, label {
        color: #4B5563;
    }

    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #E8ECF4;
        padding: 18px;
        border-radius: 22px;
        box-shadow: 0 10px 30px rgba(17, 24, 39, 0.05);
    }

    .hero-card {
        background: linear-gradient(135deg, #6C63FF 0%, #4F46E5 100%);
        border-radius: 28px;
        padding: 34px;
        color: white;
        box-shadow: 0 18px 40px rgba(79, 70, 229, 0.22);
        margin-bottom: 24px;
    }

    .hero-title {
        font-size: 44px;
        font-weight: 800;
        line-height: 1.05;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        font-size: 17px;
        line-height: 1.6;
        color: rgba(255,255,255,0.92);
        max-width: 680px;
    }

    .section-title {
        font-size: 28px;
        font-weight: 800;
        color: #111827;
        margin-top: 26px;
        margin-bottom: 14px;
        letter-spacing: -0.6px;
    }

    .soft-card {
        background: white;
        border: 1px solid #E8ECF4;
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 10px 28px rgba(17, 24, 39, 0.05);
        margin-bottom: 18px;
    }

    .mini-card {
        background: white;
        border: 1px solid #E8ECF4;
        border-radius: 22px;
        padding: 20px;
        box-shadow: 0 10px 28px rgba(17, 24, 39, 0.05);
        height: 100%;
    }

    .mini-label {
        color: #6B7280;
        font-size: 14px;
        margin-bottom: 8px;
    }

    .mini-value {
        color: #111827;
        font-size: 28px;
        font-weight: 800;
        line-height: 1.1;
    }

    .feature-title {
        font-size: 18px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 8px;
    }

    .feature-text {
        font-size: 14px;
        color: #6B7280;
        line-height: 1.6;
    }

    .pill {
        display: inline-block;
        padding: 8px 14px;
        border-radius: 999px;
        background: #EEF2FF;
        color: #4F46E5;
        font-size: 12px;
        font-weight: 700;
        margin-right: 8px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-card">
    <div class="hero-title">Find startup work that actually fits you.</div>
    <div class="hero-subtitle">
        SkillSwipe connects students with flexible, skill-based startup tasks in marketing,
        design, product, research, and more — all in one clean mobile-style experience.
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="mini-card">
        <div class="mini-label">Active startup tasks</div>
        <div class="mini-value">24</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="mini-card">
        <div class="mini-label">Top student match score</div>
        <div class="mini-value">92%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="mini-card">
        <div class="mini-label">Average task pay</div>
        <div class="mini-value">CHF 1.6k</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-title">Why SkillSwipe works</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="soft-card">
        <div class="feature-title">Student-friendly discovery</div>
        <div class="feature-text">
            Browse startup tasks in a clean feed, save the ones you like, and quickly see
            what matches your interests, availability, and skills.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="soft-card">
        <div class="feature-title">Startup-friendly hiring</div>
        <div class="feature-text">
            Startups can post short-term tasks and quickly find motivated students for research,
            design, marketing, and product support.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-title">Popular categories</div>', unsafe_allow_html=True)
st.markdown("""
<span class="pill">Marketing</span>
<span class="pill">Product</span>
<span class="pill">Design</span>
<span class="pill">Research</span>
<span class="pill">Data</span>
<span class="pill">Operations</span>
""", unsafe_allow_html=True)

st.info("Use the sidebar to open Profile, Discover Jobs, Liked Jobs, and the dashboards.")

