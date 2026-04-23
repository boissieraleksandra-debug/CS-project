import streamlit as st
from db import (
    init_db,
    get_applications_for_startup,
    update_application_status,
    update_application_task_details,
    cancel_application
)
from ui import apply_styles, header, status_badge

st.set_page_config(page_title="Applicants", page_icon="📥", layout="wide")
init_db()
apply_styles()

if st.session_state.get("role") != "startup":
    st.stop()

if "show_cancel_for" not in st.session_state:
    st.session_state.show_cancel_for = None

startup_name = st.session_state.get("startup_name", "")

header("📥 Applicants", "Manage applicants and task progress.")

applications = get_applications_for_startup(startup_name)

if not applications:
    st.info("No applications yet.")
else:
    for app in applications:
        st.markdown(f"""
        <div class="app-card">
            <div class="task-title">{app['task_title']}</div>
            <div class="task-startup">Applicant: {app['student_name']}</div>
            <div class="task-description">
                <b>Email:</b> {app['email']}<br>
                <b>Message:</b> {app['message']}<br>
                <b>Task details:</b> {app['task_details'] or '-'}<br>
                <b>Submission:</b> {app['submission_note'] or '-'}<br>
                <b>End reason:</b> {app['end_reason'] or '-'}
            </div>
            {status_badge(app['status'])}
        </div>
        """, unsafe_allow_html=True)

        status = app["status"]

        # ---------- APPLIED ----------
        if status == "Applied":
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Accept", key=f"accept_{app['id']}"):
                    update_application_status(app["id"], "Matched")
                    st.rerun()

            with col2:
                if st.button("Reject", key=f"reject_{app['id']}"):
                    update_application_status(app["id"], "Rejected")
                    st.rerun()

        # ---------- MATCHED ----------
        elif status == "Matched":
            details = st.text_area(
                "Task Instructions",
                value=app["task_details"],
                key=f"details_{app['id']}"
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Send Task Details", key=f"send_{app['id']}"):
                    update_application_task_details(app["id"], details)
                    st.success("Sent")
                    st.rerun()

            with col2:
                if st.button("End Collaboration", key=f"cancel_match_{app['id']}"):
                    st.session_state.show_cancel_for = app["id"]

        # ---------- IN PROGRESS ----------
        elif status == "In Progress":
            st.info("Student is working")

            if st.button("End Collaboration", key=f"cancel_prog_{app['id']}"):
                st.session_state.show_cancel_for = app["id"]

        # ---------- SUBMITTED ----------
        elif status == "Submitted":
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Mark Completed", key=f"complete_{app['id']}"):
                    update_application_status(app["id"], "Completed")
                    st.rerun()

            with col2:
                if st.button("End Collaboration", key=f"cancel_sub_{app['id']}"):
                    st.session_state.show_cancel_for = app["id"]

        # ---------- FINAL ----------
        elif status == "Completed":
            st.success("Completed")

        elif status == "Rejected":
            st.error("Rejected")

        elif status == "Cancelled":
            st.warning("Cancelled")

        # ---------- CANCEL FORM ----------
        if st.session_state.show_cancel_for == app["id"]:
            reason = st.text_area("Reason for ending", key=f"reason_{app['id']}")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Confirm", key=f"confirm_{app['id']}"):
                    if reason.strip():
                        cancel_application(app["id"], reason)
                        st.session_state.show_cancel_for = None
                        st.success("Ended")
                        st.rerun()
                    else:
                        st.warning("Write a reason")

            with col2:
                if st.button("Back", key=f"back_{app['id']}"):
                    st.session_state.show_cancel_for = None
                    st.rerun()
