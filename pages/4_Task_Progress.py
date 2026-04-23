import streamlit as st
from app_data import initialize_state, update_task_status, remove_applied_task
from ui import apply_global_styles, page_header, task_card_html

st.set_page_config(page_title="Task Progress", page_icon="🧩", layout="wide")

initialize_state()
apply_global_styles()
page_header("🧩 Task Progress", "Follow your saved and applied startup tasks through each stage.")

if len(st.session_state.applied_tasks) == 0:
    st.info("You haven’t applied to any tasks yet.")
else:
    for task in st.session_state.applied_tasks:
        st.markdown(task_card_html(task, show_status=True), unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("Matched", key=f"matched_{task['id']}", use_container_width=True):
                update_task_status(task["id"], "Matched")
                st.rerun()

        with col2:
            if st.button("Assigned", key=f"assigned_{task['id']}", use_container_width=True):
                update_task_status(task["id"], "Assigned")
                st.rerun()

        with col3:
            if st.button("In Progress", key=f"inprogress_{task['id']}", use_container_width=True):
                update_task_status(task["id"], "In Progress")
                st.rerun()

        with col4:
            if st.button("Completed", key=f"completed_{task['id']}", use_container_width=True):
                update_task_status(task["id"], "Completed")
                st.rerun()

        if st.button("Remove Application", key=f"remove_applied_{task['id']}", use_container_width=True):
            remove_applied_task(task["id"])
            st.rerun()
