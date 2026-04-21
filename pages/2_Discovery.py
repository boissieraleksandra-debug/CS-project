import streamlit as st

#with tells that everything that will be intented will have to be inside the box
#st.container() is function call that returns an object. And we'll be able to include some buttons inside
with st.container(border=True):
    st.subheader("Sales Manager")
    st.write("Location:", "Zurich, SUI")
    st.write("Duration:", "3 months")
    st.write("Tags:", "Sales, Revenues")
    st.write("Come and join us!")
    st.write("here")
    
