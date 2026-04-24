import streamlit as st
from db import init_db, get_all_tasks, get_saved_task_ids, remove_saved_task, create_application

st.set_page_config(page_title="Saved Tasks", page_icon="❤️", layout="wide")
init_db()

if st.session_state.get("role") != "student":
    st.warning("Please go to the home page and choose Student first.")
    st.stop()

if "show_apply_for" not in st.session_state:
    st.session_state.show_apply_for = None

st.title("❤️ Saved Tasks")

tasks = get_all_tasks()
saved_ids = set(get_saved_task_ids())
saved_tasks = [t for t in tasks if t["id"] in saved_ids]

if not saved_tasks:
    st.info("No saved tasks yet.")
else:
    for task in saved_tasks:
        st.markdown(f"""
        ### {task['title']}
        🏢 {task['startup_name']}  
        **Category:** {task['category']} | **Location:** {task['location']} | **Duration:** {task['duration']} | **Remuneration:** {task['budget']}  
        **Description:** {task['description']}
        """)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Apply Now", key=f"apply_saved_{task['id']}"):
                st.session_state.show_apply_for = task["id"]

        with col2:
            if st.button("Remove", key=f"remove_saved_{task['id']}"):
                remove_saved_task(task["id"])
                if st.session_state.show_apply_for == task["id"]:
                    st.session_state.show_apply_for = None
                st.rerun()

        if st.session_state.show_apply_for == task["id"]:
            with st.form(f"saved_apply_form_{task['id']}"):
                name = st.text_input("Full Name", value=st.session_state.get("student_name", ""))
                email = st.text_input("Email")
                phone = st.text_input("Phone")
                message = st.text_area("Short Message")
                cv = st.file_uploader("Upload CV", key=f"saved_cv_{task['id']}")

                submitted = st.form_submit_button("Submit Application")

                if submitted:
                    create_application(
                        task,
                        name,
                        email,
                        phone,
                        message,
                        cv.name if cv else "No CV"
                    )
                    remove_saved_task(task["id"])
                    st.session_state.show_apply_for = None
                    st.success("Application sent.")
                    st.rerun()

        st.divider()
