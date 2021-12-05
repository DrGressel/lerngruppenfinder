import streamlit as st
import sqlite3

def app(data):   
    class gruppe():
        def __init__(self, ersteller, studiengang, fach, tag, uhrzeit):
            self.ersteller = ersteller
            self.studiengang = studiengang
            self.fach = fach
            self.tag = tag
            self.uhrzeit = uhrzeit

    conn = sqlite3.connect('src/database.db')
    c = conn.cursor()

    try:
        c.execute("SELECT * FROM groups")
    except:
        c.execute("CREATE TABLE groups (ersteller text, studiengang text, fach text, tag text, uhrzeit text)")
        conn.commit()

    st.title('Neue Lerngruppe erstellen')

    with st.form('Lerngruppe erstellen'):
        studiengang = st.text_input('Studiengang')
        fach = st.text_input('Fach')
        tag = st.selectbox('Tag', ('Montags', 'Dienstags', 'Mittwochs', 'Donnersags', 'Freitags', 'Samstags', 'Sonntags'))
        uhrzeit = str(st.time_input('Uhrzeit'))
        NeueGruppe = gruppe(st.session_state.cu, studiengang, fach, tag, uhrzeit)
        if st.form_submit_button('Lerngruppe erstellen'):
            st.write('Lerngruppe erfolgreich erstellt')
            c.execute("INSERT INTO groups VALUES (?, ?, ?, ?, ?)", (NeueGruppe.ersteller, NeueGruppe.studiengang, NeueGruppe.fach, NeueGruppe.tag, NeueGruppe.uhrzeit))
            conn.commit()

    conn.close()