import streamlit as st
from db import init_db, get_applications_for_student, update_application_status, submit_work

st.set_page_config(page_title="Task Progress", page_icon="🧩", layout="wide")
init_db()

if st.session_state.get("role") != "student":
    st.stop()

student_name = st.session_state.get("student_name", "")

st.title("🧩 Task Progress")

apps = get_applications_for_student(student_name)

if not apps:
    st.info("No tasks yet")
else:
    for app in apps:
        st.markdown(f"""
        ### {app['task_title']}
        🏢 {app['startup_name']}  
        **Status:** {app['status']}  
        **Details:** {app['task_details'] or '-'}  
        **Submission:** {app['submission_note'] or '-'}  
        **End reason:** {app['end_reason'] or '-'}
        """)

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

        st.divider()
