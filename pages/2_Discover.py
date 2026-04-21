import streamlit as st

st.title("🔍 Discover Jobs")

jobs = [
    {
        "title": "Marketing Intern",
        "startup": "GrowthAI",
        "category": "Marketing",
        "location": "Zurich",
        "duration": "3 months",
        "pay": "CHF 1500",
        "description": "Help us grow our brand and social media presence.",
        "match": 85
    },
    {
        "title": "Product Intern",
        "startup": "TechFlow",
        "category": "Product",
        "location": "Remote",
        "duration": "6 months",
        "pay": "CHF 2000",
        "description": "Work on product features and user experience.",
        "match": 92
    },
    {
        "title": "Design Assistant",
        "startup": "CreativeLab",
        "category": "Design",
        "location": "Geneva",
        "duration": "2 months",
        "pay": "CHF 1200",
        "description": "Assist in UI/UX design and branding.",
        "match": 78
    }
]

for job in jobs:
    st.markdown(f"### {job['title']}")
    st.write(f"🏢 {job['startup']}")
    st.write(f"📍 {job['location']} | ⏳ {job['duration']}")
    st.write(f"💰 {job['pay']}")
    st.write(f"🎯 Match: {job['match']}%")
    st.write(job["description"])

    col1, col2 = st.columns(2)

    with col1:
        st.button("❌ Pass", key=job["title"] + "_pass")
    with col2:
        st.button("❤️ Like", key=job["title"] + "_like")

    st.divider()
