import streamlit as st
from app_data import initialize_state, apply_to_task, remove_saved_task
from ui import apply_global_styles, page_header, task_card_html

st.set_page_config(page_title="Saved Tasks", page_icon="❤️", layout="wide")

initialize_state()
apply_global_styles()
page_header("❤️ Saved Tasks", "Review your saved tasks and apply directly from this page.")

if len(st.session_state.saved_tasks) == 0:
    st.info("You haven’t saved any tasks yet. Go to Discover Tasks and save one first.")
else:
    for task in st.session_state.saved_tasks[:]:
        st.markdown(task_card_html(task), unsafe_allow_html=True)

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
            with st.form(f"form_{task['id']}"):
                full_name = st.text_input("Full Name", value=st.session_state.profile["full_name"])
                email = st.text_input("Email")
                phone = st.text_input("Phone Number")
                message = st.text_area("Short Message")
                cv = st.file_uploader("Upload CV", type=["pdf", "docx"], key=f"cv_{task['id']}")
                submitted = st.form_submit_button("Submit Application")

                if submitted:
                    applicant_data = {
                        "full_name": full_name,
                        "email": email,
                        "phone": phone,
                        "message": message,
                        "cv_name": cv.name if cv is not None else st.session_state.profile["cv_name"],
                    }
                    apply_to_task(task, applicant_data)
                    st.session_state.show_apply_for = None
                    st.success("Application submitted successfully.")
                    st.rerun()

