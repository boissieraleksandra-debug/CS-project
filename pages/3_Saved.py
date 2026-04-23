import streamlit as st
from data import init

init()

if st.session_state.role != "student":
    st.stop()

st.title("❤️ Saved Tasks")

for task in st.session_state.saved:
    st.markdown(f"### {task['title']}")

    if st.button("Apply", key=f"apply_saved_{task['id']}"):
        st.session_state.applications.append({
            "task_id": task["id"],
            "task_title": task["title"],
            "startup": task["startup"],
            "student": st.session_state.student["name"],
            "status": "Applied",
            "details": "",
            "submission": ""
        })
