import streamlit as st
#importing only the important features for the code.
from db import conn, init_db, create_application, save_task_for_student, get_saved_task_ids  

st.set_page_config(page_title="Discover Tasks", page_icon="🌐", layout="wide")
#initialise the database. We want to make sure that the database exists before doing anything else
init_db()

if st.session_state.get("role") != "student": 
    #memory box for the participant, it remembers his/her role and where did they click.
    #use of getter to avoid any error is the value hasn't been set
    st.warning("Please go to the home page and choose Student first.") #if the user hasn't chosen student as a role, they can't browse the job offers and need to set up a student account.
    st.stop()

st.title("🌐 Discover Tasks") #header

if "apply_task" not in st.session_state: #gives the choice to the user to apply or not
    st.session_state.apply_task = None

tasks = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
#conn. = connecting the database and execute = like placing an order but doesn't give an actual result
#FROM tasks ORDER BY id DESC = SQL (language for database), * means all columns of data (everything)
#ORDER BY id DESC = sort the data by their id descending (largest to smallest)
#Gives back the actual action
#each task is like a row

saved_ids = set(get_saved_task_ids()) #Having a set is much faster than a list.

if not tasks:
    st.info("No tasks available yet.")
else:
    for task_row in tasks:
        task = dict(task_row) #easier to work with dictionaries

        #Better to have markdown because it allows for formating, multiple lines etc
        st.markdown(f"""
        ### {task['title']}
        🏢 {task['startup_name']}  
        **Category:** {task['category']} | **Location:** {task['location']} | **Duration:** {task['duration']} | **Remunaration:** {task['budget']}  
        **Description:** {task['description']}
        """)

        col1, col2 = st.columns(2)

        #each button hss to be unique so we use a key as they are unique. It's like giving the buttons an id
        #Here we prevent dupplicates + save the choice
        with col1:
            if st.button("❤️ Save", key=f"save_{task['id']}"):
                if task["id"] in saved_ids:
                    st.info("Task already saved.")
                else:
                    save_task_for_student(task["id"])
                    st.success("Task saved.")
                    st.rerun()

        #store the selected apply button
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
            ) # This avoids error in the case there's no cv uploaded
            
            st.success("Application sent.")
            st.session_state.apply_task = None
            st.rerun()
