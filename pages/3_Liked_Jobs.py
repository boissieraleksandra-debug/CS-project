import streamlit as st

st.set_page_config(page_title="Liked Jobs", page_icon="❤️", layout="wide")

if "liked_jobs" not in st.session_state:
    st.session_state.liked_jobs = []

if "applied_jobs" not in st.session_state:
    st.session_state.applied_jobs = []

if "apply_index" not in st.session_state:
    st.session_state.apply_index = None

st.title("❤️ Liked Jobs")
st.caption("Review your saved jobs and apply when you are ready.")

if len(st.session_state.liked_jobs) == 0:
    st.info("You haven’t liked any jobs yet. Go to Discover Jobs and press Like.")
else:
    for i, job in enumerate(st.session_state.liked_jobs):
        st.markdown(f"""
        ### {job['title']}
        **🏢 {job['startup']}**  
        📂 {job['category']} | 📍 {job['location']} | ⏳ {job['duration']} | 💰 {job['pay']}  
        🎯 **{job['match']}% match**
        
        {job['description']}
        """)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Apply", key=f"apply_{i}", use_container_width=True):
                st.session_state.apply_index = i

        with col2:
            if st.button("Remove", key=f"remove_{i}", use_container_width=True):
                st.session_state.liked_jobs.pop(i)
                st.rerun()

        st.divider()

if st.session_state.apply_index is not None:
    if st.session_state.apply_index < len(st.session_state.liked_jobs):
        selected_job = st.session_state.liked_jobs[st.session_state.apply_index]

        st.subheader("Apply to this Job")
        st.write(f"Applying for **{selected_job['title']}** at **{selected_job['startup']}**")

        with st.form("application_form"):
            full_name = st.text_input("Full Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone Number")
            message = st.text_area("Short Message")
            cv = st.file_uploader("Upload CV", type=["pdf", "docx"])

            submitted = st.form_submit_button("Submit Application")

            if submitted:
                applied_job = selected_job.copy()
                applied_job["status"] = "Applied"

                st.session_state.applied_jobs.append(applied_job)
                st.session_state.liked_jobs.pop(st.session_state.apply_index)
                st.session_state.apply_index = None

                st.success("Application submitted successfully.")
                st.rerun()

st.subheader("📌 Applied Jobs")

if len(st.session_state.applied_jobs) == 0:
    st.info("You have not applied to any jobs yet.")
else:
    for job in st.session_state.applied_jobs:
        st.markdown(f"""
        ### {job['title']}
        **🏢 {job['startup']}**  
        📍 {job['location']} | 💰 {job['pay']}  
        Status: **{job['status']}**
        """)
        st.divider()

