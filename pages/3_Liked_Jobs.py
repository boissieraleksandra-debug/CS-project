import streamlit as st

st.set_page_config(page_title="Liked Jobs", page_icon="❤️", layout="wide")

if "liked_jobs" not in st.session_state:
    st.session_state.liked_jobs = []

if "applied_jobs" not in st.session_state:
    st.session_state.applied_jobs = []

if "show_form_for" not in st.session_state:
    st.session_state.show_form_for = None


def toggle_form(index):
    if st.session_state.show_form_for == index:
        st.session_state.show_form_for = None
    else:
        st.session_state.show_form_for = index


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

    .status-liked {
        background: #EF4444;
        color: white;
    }

    .status-applied {
        background: #3B82F6;
        color: white;
    }

    .section-space {
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">❤️ Liked Jobs</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Your saved startup tasks appear here. You can apply directly from this page.</div>', unsafe_allow_html=True)

# LIKED JOBS SECTION
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
            <span class="pill status-liked">Liked</span>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.button("Apply Now", key=f"apply_{i}", on_click=toggle_form, args=(i,), use_container_width=True)

        with col2:
            if st.button("Remove", key=f"remove_{i}", use_container_width=True):
                st.session_state.liked_jobs.pop(i)
                if st.session_state.show_form_for == i:
                    st.session_state.show_form_for = None
                st.rerun()

        if st.session_state.show_form_for == i:
            st.markdown("## Application Form")

            with st.form(f"application_form_{i}"):
                name = st.text_input("Full Name", key=f"name_{i}")
                email = st.text_input("Email", key=f"email_{i}")
                phone = st.text_input("Phone Number", key=f"phone_{i}")
                cv = st.file_uploader("Upload your CV", type=["pdf", "docx"], key=f"cv_{i}")

                submitted = st.form_submit_button("Submit Application")

                if submitted:
                    applied_job = job.copy()
                    applied_job["status"] = "Applied"
                    applied_job["applicant_name"] = name
                    applied_job["email"] = email
                    applied_job["phone"] = phone
                    applied_job["cv_name"] = cv.name if cv is not None else "No CV uploaded"

                    st.session_state.applied_jobs.append(applied_job)
                    st.session_state.liked_jobs.pop(i)
                    st.session_state.show_form_for = None

                    st.success("Application submitted successfully!")
                    st.rerun()

            if st.button("Cancel", key=f"cancel_{i}", use_container_width=True):
                st.session_state.show_form_for = None
                st.rerun()

# APPLIED JOBS SECTION
st.markdown('<div class="section-space"></div>', unsafe_allow_html=True)
st.markdown("## 📩 Applied Jobs")

if len(st.session_state.applied_jobs) == 0:
    st.info("You haven’t applied to any jobs yet.")
else:
    for j, job in enumerate(st.session_state.applied_jobs):
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
            <span class="pill status-applied">Applied</span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Remove Application", key=f"remove_applied_{j}", use_container_width=True):
            st.session_state.applied_jobs.pop(j)
            st.rerun()

