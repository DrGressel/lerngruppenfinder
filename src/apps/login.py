import streamlit as st
import sqlite3

def app(data):
    class User():
        def __init__(self, username, password):
            self.username = username
            self.password = password

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    conn = sqlite3.connect('src/user_database.db')
    c = conn.cursor()

    try:
        c.execute("SELECT * FROM users")
    except:
        c.execute("CREATE TABLE users (username text, password text)")
        conn.commit()
    

    st.title('Log in/ Registrieren')
    nutzercount = list(c.execute("SELECT COUNT(*) FROM users"))
    st.write('Registrierte Nutzer:', nutzercount[-1][0])
    option = st.selectbox('Log in/ Registrieren', ('Log in', 'Registrieren'))

    if option == 'Log in':
        with st.form('Log in'):
            username = st.text_input('Nutzername')
            password = st.text_input('Passwort', type = 'password')
            ExistingUser = User(username, password)
            if st.form_submit_button('Log in'):
                if list(c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (ExistingUser.username, ExistingUser.password))):
                    st.session_state.logged_in = True
                    st.write('Du hast dich erfolgreich angemeldet!')
                    st.experimental_rerun()
                else:
                    st.write('Nutzername oder Passwort flasch!')

    else:
        with st.form('Registrieren'):
            username = st.text_input('Nutzername')
            password = st.text_input('Passwort', type = 'password')
            NewUser = User(username, password)
            if st.form_submit_button('Registrieren'):
                if len(password) < 4:
                    st.write('Dein Passwort muss mindestens 4 Zeichen haben.')
                else:
                    if list(c.execute("SELECT * FROM users WHERE username = ?", (NewUser.username,))):
                        st.write('Dieser Nutzername ist schon vergeben.')
                    else:
                        c.execute("INSERT INTO users VALUES (?, ?)", (NewUser.username, NewUser.password))
                        conn.commit()
                        st.write('Nutzer erfolgreich angelegt! Du kannst dich jetzt anmelden.')

    #st.subheader('Gesamte Datenbank')
    #ergebnis = list(c.execute("SELECT * FROM users"))
    #st.write(ergebnis)

    conn.close()