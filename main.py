import streamlit as st
from gsheetsdb import connect
import pandas as pd
from datetime import datetime as dt

# Create a connection object.
st.set_page_config(layout="wide")

with st.sidebar:
    display_table = st.checkbox("show table")

conn = connect()

st.title("Pflanzensensor Datenanalyse")

class Sensor_data:
    def __init__(self, sheet_url, df):
       self.sheet_url = sheet_url
       self.df = df

    #@st.cache(suppress_st_warning=True)
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
        df_line = self.df
        df_line["Datum"] = pd.to_datetime(df_line["Datum"]).dt.strftime("%H:%M")
        st.line_chart(df_line, x = x,)

    def show_metric(self):
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label="Temperature", value=str(self.df.iloc[-1]["Temperatur"])+"°C", delta=str((int(self.df.iloc[-1]["Temperatur"]))-int(self.df.iloc[-2]["Temperatur"]))+"°C")
        col2.metric(label="Moisture", value=str(self.df.iloc[-1]["Feuchtigkeit"])+"", delta=str((int(self.df.iloc[-1]["Feuchtigkeit"]))-int(self.df.iloc[-2]["Feuchtigkeit"]))+"")
        col3.metric(label="Light", value=str(self.df.iloc[-1]["Licht"])+"", delta=str((int(self.df.iloc[-1]["Licht"]))-int(self.df.iloc[-2]["Licht"]))+"")
        col4.metric(label="Conductivity", value=str(self.df.iloc[-1]["Leitfähigkeit"])+"", delta=str((int(self.df.iloc[-1]["Leitfähigkeit"]))-int(self.df.iloc[-2]["Leitfähigkeit"]))+"")

df = pd.DataFrame(columns=["Datum","Temperatur","Feuchtigkeit","Licht","Leitfähigkeit"])
sheet_url = st.secrets["public_gsheets_url"]

sd = Sensor_data(sheet_url, df)
sd.run_query()
sd.show_metric()

if display_table:
    sd.show_table()
    sd.show_line(x="Time")
else:
    sd.show_line(x="Time")

