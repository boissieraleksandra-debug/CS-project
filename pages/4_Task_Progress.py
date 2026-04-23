import streamlit as st
from db import (
    init_db,
    get_applications_for_student,
    update_application_status,
    submit_work
)
from ui import apply_styles, header, status_badge

st.set_page_config(page_title="Task Progress", page_icon="🧩", layout="wide")
init_db()
apply_styles()

if st.session_state.get("role") != "student":
    st.stop()

student_name = st.session_state.get("student_name", "")

header("🧩 Task Progress", "Track your work")

apps = get_applications_for_student(student_name)

if not apps:
    st.info("No tasks yet")
else:
    for app in apps:
        st.markdown(f"""
        <div class="app-card">
            <div class="task-title">{app['task_title']}</div>
            <div class="task-startup">{app['startup_name']}</div>
            <div class="task-description">
                <b>Details:</b> {app['task_details'] or '-'}<br>
                <b>Submission:</b> {app['submission_note'] or '-'}<br>
                <b>End reason:</b> {app['end_reason'] or '-'}
            </div>
            {status_badge(app['status'])}
        </div>
        """, unsafe_allow_html=True)

        if app["status"] == "Matched":
            if st.button("Start Task", key=f"start_{app['id']}"):
                update_application_status(app["id"], "In Progress")
                st.rerun()

        if app["status"] == "In Progress":
            with st.form(f"submit_{app['id']}"):
                note = st.text_area("Work description")
                link = st.text_input("Link")
                if st.form_submit_button("Submit"):
                    submit_work(app["id"], note, link)
                    st.success("Submitted")
                    st.rerun()
