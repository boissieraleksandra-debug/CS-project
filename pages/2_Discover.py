import streamlit as st

st.set_page_config(page_title="Discover Jobs", page_icon="🔍", layout="wide")

if "liked_jobs" not in st.session_state:
    st.session_state.liked_jobs = []

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

st.title("🔍 Discover Jobs")
st.caption("Browse startup tasks and save the ones you like.")

for i, job in enumerate(jobs):
    st.markdown(f"""
    ### {job['title']}
    **🏢 {job['startup']}**  
    📂 {job['category']} | 📍 {job['location']} | ⏳ {job['duration']} | 💰 {job['pay']}  
    🎯 **{job['match']}% match**
    
    {job['description']}
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.button("❌ Pass", key=f"pass_{i}", use_container_width=True)

    with col2:
        if st.button("❤️ Like", key=f"like_{i}", use_container_width=True):
            already_liked = any(
                liked_job["title"] == job["title"] and liked_job["startup"] == job["startup"]
                for liked_job in st.session_state.liked_jobs
            )

            if not already_liked:
                st.session_state.liked_jobs.append(job)
                st.success(f"You liked {job['title']} at {job['startup']}.")
            else:
                st.info("This job is already in your liked jobs.")

    st.divider()

             
