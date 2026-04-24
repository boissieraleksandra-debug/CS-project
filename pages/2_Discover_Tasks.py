import streamlit as st
#importing only the important features for the code.
from db import conn, init_db, create_application, save_task_for_student, get_saved_task_ids  

st.set_page_config(page_title="Discover Tasks", page_icon="🔍", layout="wide")
#initialise the database. We want to make sure that the database exists before doing anything else
init_db()

if st.session_state.get("role") != "student": 
    #memory box for the participant, it remembers his/her role and where did they click.
    #use of getter to avoid any error is the value hasn't been set
    st.warning("Please go to the home page and choose Student first.") #if the user hasn't chosen student as a role, they can't browse the job offers and need to set up a student account.
    st.stop()

st.title("🔍 Discover Tasks") #header

if "apply_task" not in st.session_state: #gives the choice to the user to apply or not
    st.session_state.apply_task = None

tasks = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
saved_ids = set(get_saved_task_ids())

if not tasks:
    st.info("No tasks available yet.")
else:
    for task_row in tasks:
        task = dict(task_row)

        st.markdown(f"""
        ### {task['title']}
        🏢 {task['startup_name']}  
        📂 {task['category']} | 📍 {task['location']} | ⏳ {task['duration']} | 💰 {task['budget']}  
        {task['description']}
        """)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("❤️ Save", key=f"save_{task['id']}"):
                if task["id"] in saved_ids:
                    st.info("Task already saved.")
                else:
                    save_task_for_student(task["id"])
                    st.success("Task saved.")
                    st.rerun()

        with col2:
            if st.button("Apply", key=f"apply_{task['id']}"):
                st.session_state.apply_task = task

        st.divider()

if st.session_state.apply_task is not None:
    task = st.session_state.apply_task

    st.subheader(f"Apply to {task['title']}")

    with st.form("apply_form"):
        name = st.text_input("Full Name", value=st.session_state.get("student_name", ""))
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        message = st.text_area("Short Message")
        cv = st.file_uploader("Upload CV")

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

            st.success("Application sent.")
            st.session_state.apply_task = None
            st.rerun()
