import streamlit as st

st.set_page_config(page_title="Profile", page_icon="👤", layout="wide")

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
        margin-bottom: 24px;
    }

    .profile-card {
        background: white;
        border: 1px solid #E8ECF4;
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 10px 28px rgba(17, 24, 39, 0.05);
        margin-bottom: 18px;
    }

    .avatar-card {
        background: linear-gradient(135deg, #6C63FF 0%, #4F46E5 100%);
        border-radius: 26px;
        padding: 28px;
        color: white;
        box-shadow: 0 18px 40px rgba(79, 70, 229, 0.20);
        text-align: center;
        min-height: 220px;
    }

    .avatar-circle {
        width: 88px;
        height: 88px;
        border-radius: 50%;
        background: rgba(255,255,255,0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 16px auto;
        font-size: 34px;
        font-weight: 800;
    }

    .avatar-name {
        font-size: 24px;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .avatar-subtext {
        font-size: 14px;
        color: rgba(255,255,255,0.88);
        line-height: 1.5;
    }

    .section-label {
        font-size: 20px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 12px;
    }

    [data-testid="stTextInput"] > div,
    [data-testid="stTextArea"] > div,
    [data-testid="stSelectbox"] > div,
    [data-testid="stFileUploader"] {
        border-radius: 14px;
    }

    .hint-card {
        background: #EEF2FF;
        color: #4338CA;
        border-radius: 18px;
        padding: 14px 16px;
        font-size: 14px;
        font-weight: 600;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">👤 My Profile</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Build a student profile that helps the app recommend the best startup tasks for you.</div>', unsafe_allow_html=True)

left, right = st.columns([1, 2])

with left:
    st.markdown("""
    <div class="avatar-card">
        <div class="avatar-circle">A</div>
        <div class="avatar-name">Aleksandra</div>
        <div class="avatar-subtext">
            Marketing-minded student looking for flexible startup work in product, research, and growth.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hint-card">
        Tip: profiles with clear interests and availability usually get better recommendations.
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown('<div class="profile-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Basic information</div>', unsafe_allow_html=True)

    full_name = st.text_input("Full Name", placeholder="Enter your full name")
    linkedin = st.text_input("LinkedIn", placeholder="Paste your LinkedIn profile URL")

    col1, col2 = st.columns(2)
    with col1:
        education = st.selectbox(
            "Education",
            ["Select", "Business", "Marketing", "Design", "Economics", "Computer Science", "Other"]
        )
    with col2:
        availability = st.selectbox(
            "Availability",
            ["Select", "Part-time", "Flexible", "Weekends", "Evenings", "Full-time"]
        )

    interests = st.text_area(
        "Interests",
        placeholder="Example: branding, social media, product strategy, user research",
        height=120
    )

    about = st.text_area(
        "Short Description",
        placeholder="Tell startups a bit about yourself, what you enjoy working on, and what kind of tasks interest you.",
        height=120
    )

    cv = st.file_uploader("Upload CV", type=["pdf", "docx"])

    st.button("Save Profile", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
