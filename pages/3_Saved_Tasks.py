import streamlit as st
from db import (
    init_db, get_all_tasks, get_saved_task_ids, remove_saved_task,
    create_application, get_student_profile
)
from ui import apply_styles, header, task_card

st.set_page_config(page_title="Saved Tasks", page_icon="❤️", layout="wide")
init_db()
apply_styles()

if st.session_state.get("role") != "student":
    st.stop()

if "show_apply_for" not in st.session_state:
    st.session_state.show_apply_for = None

header("❤️ Saved Tasks", "Review your saved tasks and apply directly from here.")

profile = get_student_profile()
tasks = get_all_tasks()
saved_ids = set(get_saved_task_ids())
saved_tasks = [t for t in tasks if t["id"] in saved_ids]

if not saved_tasks:
    st.info("You haven’t saved any tasks yet.")
else:
    for task in saved_tasks:
        st.markdown(task_card(task), unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Apply Now", key=f"apply_{task['id']}", use_container_width=True):
                st.session_state.show_apply_for = task["id"]

        with col2:
            if st.button("Remove", key=f"remove_{task['id']}", use_container_width=True):
                remove_saved_task(task["id"])
                if st.session_state.show_apply_for == task["id"]:
                    st.session_state.show_apply_for = None
                st.rerun()

        if st.session_state.show_apply_for == task["id"]:
            st.markdown("### Application Form")
            with st.form(f"apply_form_{task['id']}"):
                full_name = st.text_input("Full Name", value=profile["full_name"])
                email = st.text_input("Email")
                phone = st.text_input("Phone Number")
                message = st.text_area("Short Message")
                cv = st.file_uploader("Upload CV", type=["pdf", "docx"], key=f"cv_{task['id']}")
                submitted = st.form_submit_button("Submit Application")

                if submitted:
                    create_application({
                        "task_id": task["id"],
                        "task_title": task["title"],
                        "startup_name": task["startup_name"],
                        "student_name": full_name,
                        "email": email,
                        "phone": phone,
                        "message": message,
                        "cv_name": cv.name if cv is not None else profile["cv_name"],
                        "status": "Applied",
                    })
                    remove_saved_task(task["id"])
                    st.session_state.show_apply_for = None
                    st.success("Application submitted successfully.")
                    st.rerun()
