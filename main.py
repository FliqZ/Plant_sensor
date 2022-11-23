import streamlit as st
from gsheetsdb import connect
import pandas as pd
import altair as alt
from datetime import datetime as dt

class Sensor_data:
    def __init__(self, sheet_url, df):
       self.sheet_url = sheet_url
       self.df = df

    def run_query(self):
        query = f'SELECT * FROM "{self.sheet_url}"'
        rows = conn.execute(query, headers=1)
        rows = rows.fetchall()
        self.rows = rows

        for row in self.rows:
            self.df.loc[len(self.df)] = row

    def show_table(self):
        self.df.drop("Battery", inplace=True, axis=1)
        st.write(self.df.tail(24))

    #Displays a line chart, the variable show_time_history specifies how many time entries are displayed on the x-axis
    def show_line(self, x):
        df_line = self.df.tail(show_time_history)
        try:
            df_line.drop("Battery", inplace=True, axis=1)
        except KeyError:
            pass 
        st.line_chart(df_line, x = x, y = selected_columns, use_container_width=True,height=0)

    #Displays the current value and the delta to the last value
    def show_metric(self):
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label="Temperature", value=str(self.df.iloc[-1]["Temperature"])+"°C", delta=str(round((float(self.df.iloc[-1]["Temperature"]))-float(self.df.iloc[-2]["Temperature"]),2))+"°C")
        col2.metric(label="Moisture", value=str(self.df.iloc[-1]["Moisture"])+"%", delta=str(round((float(self.df.iloc[-1]["Moisture"]))-float(self.df.iloc[-2]["Moisture"]),2))+"%")
        col3.metric(label="Light", value=str(self.df.iloc[-1]["Light"])+"lux", delta=str(round((float(self.df.iloc[-1]["Light"]))-float(self.df.iloc[-2]["Light"]),2))+"lux")
        col4.metric(label="Conductivity", value=str(self.df.iloc[-1]["Conductivity"])+"[µS/cm]", delta=str(round((float(self.df.iloc[-1]["Conductivity"]))-float(self.df.iloc[-2]["Conductivity"]),2))+"[µS/cm]")

    def show_battery(self):
        st.title(":battery:" + str(int(self.df.iloc[-1]["Battery"]))+"%")

#Layout and Title
st.set_page_config(layout="wide")
st.title("Plant sensor - data analysis :seedling:")

#Define the Sidebar
with st.sidebar:
    show_time_history = st.slider("Show the last hours", 2, 24, 10)
    selected_columns = st.multiselect("Which values should be displayed?",["Temperature","Moisture","Light","Conductivity"])
    display_table = st.checkbox("show table")

#Connection object for gspread
conn = connect()

#Parameter for class Sensor_data 
df = pd.DataFrame(columns=["Time","Temperature","Moisture","Light","Conductivity","Battery"])
#st.secrets gets value from streamlit cloud (url from the sheet)
sheet_url = st.secrets["public_gsheets_url"]

sd = Sensor_data(sheet_url, df)
sd.run_query()
sd.show_battery()
sd.show_metric()

if display_table:
    sd.show_table()
    sd.show_line(x="Time")
else:
    sd.show_line(x="Time")


