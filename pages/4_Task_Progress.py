import streamlit as st
from db import init_db, get_student_profile, get_applications_for_student, update_application_status, submit_work
from ui import apply_styles, header, status_badge

st.set_page_config(page_title="Task Progress", page_icon="🧩", layout="wide")
init_db()
apply_styles()

if st.session_state.get("role") != "student":
    st.stop()

profile = get_student_profile()
student_name = profile["full_name"]

header("🧩 Task Progress", "Track every task from application to completion.")

if not student_name:
    st.warning("Please save your student profile first.")
    st.stop()

applications = get_applications_for_student(student_name)

if not applications:
    st.info("You haven’t applied to any tasks yet.")
else:
    for app in applications:
        st.markdown(f"""
        <div class="app-card">
            <div class="task-title">{app['task_title']}</div>
            <div class="task-startup">🏢 {app['startup_name']}</div>
            <div class="task-description">
                <b>Message:</b> {app['message'] or '-'}<br>
                <b>Task details:</b> {app['task_details'] or 'No detailed instructions yet.'}<br>
                <b>Submission note:</b> {app['submission_note'] or '-'}<br>
                <b>Submission link:</b> {app['submission_link'] or '-'}
            </div>
            {status_badge(app['status'])}
        </div>
        """, unsafe_allow_html=True)

        if app["status"] == "Matched":
            if st.button("Start Task", key=f"start_{app['id']}", use_container_width=True):
                update_application_status(app["id"], "In Progress")
                st.rerun()

        if app["status"] == "In Progress":
            with st.form(f"submit_work_{app['id']}"):
                note = st.text_area("Describe what you completed")
                link = st.text_input("Paste a link to your work")
                submitted = st.form_submit_button("Submit Work")
                if submitted:
                    submit_work(app["id"], note, link)
                    st.success("Work submitted.")
                    st.rerun()
