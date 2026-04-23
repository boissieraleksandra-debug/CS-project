import streamlit as st
from db import (
    init_db, get_startup_profile, get_applications_for_startup,
    update_application_status, update_application_task_details
)
from ui import apply_styles, header, status_badge

st.set_page_config(page_title="Applicants", page_icon="📥", layout="wide")
init_db()
apply_styles()

if st.session_state.get("role") != "startup":
    st.stop()

profile = get_startup_profile()
startup_name = profile["startup_name"]

header("📥 Applicants", "Review applications, match students, send details, and complete work.")

if not startup_name:
    st.warning("Please save your startup profile first.")
    st.stop()

applications = get_applications_for_startup(startup_name)

if not applications:
    st.info("No students have applied yet.")
else:
    for app in applications:
        st.markdown(f"""
        <div class="app-card">
            <div class="task-title">{app['task_title']}</div>
            <div class="task-startup">Applicant: {app['student_name']}</div>
            <div class="task-description">
                <b>Email:</b> {app['email'] or '-'}<br>
                <b>Phone:</b> {app['phone'] or '-'}<br>
                <b>Message:</b> {app['message'] or '-'}<br>
                <b>CV:</b> {app['cv_name'] or '-'}<br>
                <b>Task details sent:</b> {app['task_details'] or 'No details sent yet.'}<br>
                <b>Submission note:</b> {app['submission_note'] or '-'}<br>
                <b>Submission link:</b> {app['submission_link'] or '-'}
            </div>
            {status_badge(app['status'])}
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        with c1:
            if st.button("Accept", key=f"accept_{app['id']}", use_container_width=True):
                update_application_status(app["id"], "Matched")
                st.rerun()

        with c2:
            if st.button("Reject", key=f"reject_{app['id']}", use_container_width=True):
                update_application_status(app["id"], "Rejected")
                st.rerun()

        if app["status"] == "Matched":
            details = st.text_area(
                "Send detailed task instructions",
                value=app["task_details"],
                key=f"details_{app['id']}"
            )
            if st.button("Send Task Details", key=f"send_{app['id']}", use_container_width=True):
                update_application_task_details(app["id"], details)
                st.success("Task details sent.")
                st.rerun()

        if app["status"] == "Submitted":
            if st.button("Mark Completed", key=f"complete_{app['id']}", use_container_width=True):
                update_application_status(app["id"], "Completed")
                st.rerun()
