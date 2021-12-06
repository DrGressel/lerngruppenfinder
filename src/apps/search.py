import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

def app(data):
    st.title('Lerngruppe suchen')

    conn = sqlite3.connect('src/database.db')
    c = conn.cursor()

    try:
        c.execute("SELECT * FROM groups")
    except:
        c.execute("CREATE TABLE groups (ersteller text, studiengang text, fach text, tag text, uhrzeit text)")
        conn.commit()    

    gruppencount = len(list(c.execute("SELECT * FROM groups")))
    st.metric(label = 'Lerngruppen insg.', value = gruppencount)

    ergebnis = list(c.execute("SELECT * FROM groups"))
    df = pd.DataFrame.from_records(ergebnis, index = None, columns = ['Ersteller', 'Studiengang', 'Fach', 'Tag', 'Uhrzeit'], coerce_float=False, nrows=None)
    st.dataframe(df)

    st.subheader('Top Lerngruppen ersteller')
    auswertung = df['Ersteller'].value_counts()
    fig = px.pie(auswertung, values = 'Ersteller', names = auswertung.index)
    st.plotly_chart(fig)

    conn.close()