#this page is the profiling section of the app 
#====================================================
import streamlit as st
import json   # built-in library to read and write JSON files
import os   # built-in library for handling folders
#this part means that if no button was chosen the opening page should be shown
if "role" not in st.session_state:
    st.session_state.role = None
#the part below is making hte difference between when the user is viewing the final profile or editing it 
if "mode" not in st.session_state:
    st.session_state.mode = "edit"
#====================================================
#FORM for profile for students
#====================================================
if st.session_state.role is None:
    st.title("Welcome!")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎓 I'm a student", use_container_width=True):
            st.session_state.role = "student"
            st.rerun()

    with col2:
        if st.button("🚀 I'm a startup", use_container_width=True):
            st.session_state.role = "startup"
            st.rerun()

#now we create the opening of the form once the user clicks on the button student
if st.session_state.role == "student" and st.session_state.mode == "edit":
    st.title("🎓 Student Profile")
    
    full_name = st.text_input("Full name")
#second part of the form because we ask for the linkedin and university (same structure as name because we want the user to fill it out completely) and needs to be on the same allignment as the full name because it is part of the if statement 

    LinkedIn = st.text_input("LinkedIn profile URL")
    Education = st.text_input("Current curriculum and name of the university")
#okay now we have to use sth different because we want the user to choose between several options and not write sth down 
    Interests = st.multiselect(
        "Your interests",
        options=[
            "Marketing",
            "Finance",
            "Technology",
            "Design",
            "Data & Analytics",
            "Legal",
            "Human Resources",
            "Coding",
            "Consulting",
            "Sustainability",
        ],
    )
#now its more or less the same as the one with interest but we want the user to only choose one option and not multiple 
    Availability = st.selectbox(
        "Availability",
        options=[
            "Less than 5 hours / week",
            "5-10 hours / week",
            "10-20 hours / week",
            "Full-time",
            "Weekends only",
        ],
    )
#now we want to put the picture feature, it is different because the user has to upload sth 
    Photo = st.file_uploader(
        "Profile picture",
        type=["png", "jpg", "jpeg"],
    )
    if Photo is not None:
        st.image(Photo, width=150)
#okay now we do the same but for the CV 
    cv_file = st.file_uploader(
        "Upload your CV (PDF)",
        type=["pdf"],
    )
    if cv_file is not None:
        st.write(f"CV Uploaded: {cv_file.name}")

#now what we are doing is again creating a two columns thing to add a "back" and a "save profile" button
    col_back, col_save_profile = st.columns(2)

    with col_back: 
        if st.button("Back", use_container_width=True):
            st.session_state.role = None #you forget the chosen role 
            st.session_state.mode = "edit" #reset to edit for next time 
            st.rerun()
    
    #when the user wants to save its profile 
    with col_save_profile: 
        if st.button("Save Profile", use_container_width=True):
            # 0. Make sure the folders exist (create them if missing)
            os.makedirs("data/photos", exist_ok=True)
            os.makedirs("data/cvs", exist_ok=True)
            # 1. Read the existing profiles.json into a Python list
            with open("data/profiles.json", "r") as f:
                profiles = json.load(f)

            # 2. Make a unique ID for this new student (e.g. student_1)
            student_count = len([p for p in profiles if p["role"] == "student"])
            new_id = f"student_{student_count + 1}"

            # 3. Save the uploaded photo to data/photos/ if one was uploaded
            photo_path = None
            if Photo is not None:
                photo_path = f"data/photos/{new_id}.png"
                with open(photo_path, "wb") as f:
                    f.write(Photo.getvalue())

            # 4. Save the uploaded CV to data/cvs/ if one was uploaded
            cv_path = None
            if cv_file is not None:
                cv_path = f"data/cvs/{new_id}.pdf"
                with open(cv_path, "wb") as f:
                    f.write(cv_file.getvalue())

            # 5. Build the new profile dictionary
            new_profile = {
                "id": new_id,
                "role": "student",
                "full_name": full_name,
                "linkedin": LinkedIn,
                "education": Education,
                "interests": Interests,
                "availability": Availability,
                "photo_path": photo_path,
                "cv_path": cv_path,
            }

            # 6. Append the new profile and write the whole list back to the file
            profiles.append(new_profile)
            with open("data/profiles.json", "w") as f:
                json.dump(profiles, f, indent=2)

            # 7. Also save to session_state for the view page
            st.session_state.full_name = full_name 
            st.session_state.LinkedIn = LinkedIn 
            st.session_state.Education = Education 
            st.session_state.Interests = Interests 
            st.session_state.Availability = Availability
            st.session_state.Photo = Photo 
            st.session_state.cv_file = cv_file 
            st.session_state.new_id = new_id

            # 8. Switch to view mode
            st.session_state.mode = "view"
            st.rerun() 
    
    
       