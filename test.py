import streamlit as st

st.button("wut", type="primary")
if st.button("CLICK"):
    st.success("Clicked!")
else:
    st.warning("Not Clicked..")


