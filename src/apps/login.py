import streamlit as st
import sqlite3
import bcrypt
import datetime

def app(data):
    class User():
        def __init__(self, username, password):
            self.username = username
            self.password = password

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.cu = None

    conn = sqlite3.connect('src/database.db')
    c = conn.cursor()

    try:
        c.execute("SELECT * FROM users")
    except:
        c.execute("CREATE TABLE users (time text, username text, password text)")
        conn.commit()
    
    st.title('Log in/ Registrieren')
    nutzercount = len(list(c.execute("SELECT * FROM users")))
    st.metric(label = 'Registrierte Nutzer', value = nutzercount)

    option = st.selectbox('Bitte auswählen', ('Log in', 'Registrieren'))

    if option == 'Log in':
        with st.form('Log in'):
            username = st.text_input('Nutzername')
            password = st.text_input('Passwort', type = 'password')
            bpassword = bytes(password, 'utf-8')
            ExistingUser = User(username, bpassword)
            if st.form_submit_button('Log in'):
                ergebnis = list(c.execute("SELECT * FROM users WHERE username = ?", (ExistingUser.username,)))
                if ergebnis and bcrypt.checkpw(ExistingUser.password, ergebnis[0][2]):
                    st.session_state.logged_in = True
                    st.session_state.cu = username
                    st.write(st.session_state.cu)
                    st.experimental_rerun()
                else:
                    st.write('Nutzername oder Passwort flasch!')

    else:
        with st.form('Registrieren'):
            username = st.text_input('Nutzername')
            password = st.text_input('Passwort', type = 'password')
            bpassword = bytes(password, 'utf-8')
            hpassword = bcrypt.hashpw(bpassword, bcrypt.gensalt())
            NewUser = User(username, hpassword)
            if st.form_submit_button('Registrieren'):
                st.session_state.logged_in = False
                if len(password) < 4:
                    st.write('Dein Passwort muss mindestens 4 Zeichen haben.')
                else:
                    if list(c.execute("SELECT * FROM users WHERE username = ?", (NewUser.username,))):
                        st.write('Dieser Nutzername ist schon vergeben.')
                    else:
                        c.execute("INSERT INTO users VALUES (?, ?, ?)", (datetime.datetime.now(), NewUser.username, NewUser.password))
                        conn.commit()
                        st.write('Nutzer erfolgreich angelegt! Du kannst dich jetzt anmelden.')

    conn.close()