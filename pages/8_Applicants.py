import streamlit as st
from db import (
    init_db,
    get_applications_for_startup,
    update_application_status,
    update_application_task_details,
    cancel_application
)

st.set_page_config(page_title="Applicants", page_icon="📥", layout="wide")
init_db()

if st.session_state.get("role") != "startup":
    st.warning("Please go to the home page and choose Startup first.")
    st.stop()

if "show_cancel_for" not in st.session_state:
    st.session_state.show_cancel_for = None

startup_name = st.session_state.get("startup_name", "")

st.title("📥 Applicants")

if not startup_name:
    st.info("Please save your startup profile first.")
    st.stop()

applications = get_applications_for_startup(startup_name)

if not applications:
    st.info("No applications yet.")
else:
    for app in applications:
        st.markdown(f"""
        ### {app['task_title']}
        Student: {app['student_name']}  
        Email: {app['email']}  
        Message: {app['message']}  
        Status: {app['status']}  
        Task details: {app['task_details'] or '-'}  
        Submission: {app['submission_note'] or '-'}  
        End reason: {app['end_reason'] or '-'}
        """)

        status = app["status"]

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

        elif status == "Matched":
            details = st.text_area("Task Instructions", value=app["task_details"], key=f"details_{app['id']}")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Send Task Details", key=f"send_{app['id']}"):
                    update_application_task_details(app["id"], details)
                    st.success("Sent")
                    st.rerun()

            with col2:
                if st.button("End Collaboration", key=f"cancel_match_{app['id']}"):
                    st.session_state.show_cancel_for = app["id"]

        elif status == "In Progress":
            st.info("Student is working")

            if st.button("End Collaboration", key=f"cancel_progress_{app['id']}"):
                st.session_state.show_cancel_for = app["id"]

        elif status == "Submitted":
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Mark Completed", key=f"complete_{app['id']}"):
                    update_application_status(app["id"], "Completed")
                    st.rerun()

            with col2:
                if st.button("End Collaboration", key=f"cancel_submitted_{app['id']}"):
                    st.session_state.show_cancel_for = app["id"]

        elif status == "Completed":
            st.success("Completed")

        elif status == "Rejected":
            st.error("Rejected")

        elif status == "Cancelled":
            st.warning("Cancelled")

        if st.session_state.show_cancel_for == app["id"]:
            reason = st.text_area("Reason for ending", key=f"reason_{app['id']}")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Confirm", key=f"confirm_cancel_{app['id']}"):
                    if reason.strip():
                        cancel_application(app["id"], reason)
                        st.session_state.show_cancel_for = None
                        st.success("Ended")
                        st.rerun()
                    else:
                        st.warning("Write a reason")

            with col2:
                if st.button("Back", key=f"back_cancel_{app['id']}"):
                    st.session_state.show_cancel_for = None
                    st.rerun()

        st.divider()
