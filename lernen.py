from src.utils.MultiPage import MultiPage
from src.apps import login, logout, search
import streamlit as st

st.set_page_config(
    page_title="Lerngruppenfinder",
    #page_icon="",
    #layout="wide",
    initial_sidebar_state="expanded",
)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

app = MultiPage()
if st.session_state.logged_in == True:
    app.add_app('Log in', login.app)
    app.add_app('Lerngruppe suchen', search.app)
    app.add_app('Log out', logout.app)
else:
    app.add_app('Log in', login.app)
app.run()
