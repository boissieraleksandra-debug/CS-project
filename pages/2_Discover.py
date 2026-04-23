import streamlit as st
from data import init

init()

if st.session_state.role != "student":
    st.stop()

st.title("🔍 Discover Tasks")

for task in st.session_state.tasks:
    st.markdown(f"### {task['title']}")
    st.write(task["description"])
    st.write(f"Startup: {task['startup']}")

    col1, col2 = st.columns(2)

    if col1.button("❤️ Save", key=f"s{task['id']}"):
        st.session_state.saved.append(task)

    if col2.button("Apply", key=f"a{task['id']}"):
        st.session_state.applications.append({
            "task_id": task["id"],
            "task_title": task["title"],
            "startup": task["startup"],
            "student": st.session_state.student["name"],
            "status": "Applied",
            "details": "",
            "submission": ""
        })
