import streamlit as st
from gsheetsdb import connect
import pandas as pd

# Create a connection object.
conn = connect()

st.title("Pflanzensensor Datenaufbereitung")

class Sensor_data:
    def __init__(self, sheet_url, df):
       self.sheet_url = sheet_url
       self.df = df
    
    @st.cache(ttl=600)
    def run_query(self):
        query = f'SELECT * FROM "{self.sheet_url}"'
        rows = conn.execute(query, headers=1)
        rows = rows.fetchall()
        self.rows = rows

        for row in self.rows:
            self.df.loc[len(self.df)] = row

    def show_table(self):
        st.write(self.df)

    def show_line(self, x):
        st.line_chart(self.df, x = x)

df = pd.DataFrame(columns=["Datum","Temperatur","Feuchtigkeit","Licht","Leitfähigkeit"])
sheet_url = st.secrets["public_gsheets_url"]

sd = Sensor_data(sheet_url, df)
sd.run_query()
sd.show_table()
sd.show_line(x="Datum")