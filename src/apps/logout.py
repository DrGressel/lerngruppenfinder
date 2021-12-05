import streamlit as st

def app(data):
    st.session_state.logged_in = False
    st.experimental_rerun()