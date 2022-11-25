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

    #Displays a line chart, the variable show_time_history specifies how many time entries are displayed on the x-axis
    def show_line(self):
        
        scale_date_1 = self.df.iloc[-1]["Time"]
        
        scale_date_1 = dt.strptime(scale_date_1,"%c").time().hour

        df_line = self.df.tail(scale_date_1+1)

        col1, col2, col3, col4 = st.columns(4)

        chart1 = alt.Chart(df_line).mark_line(point={"filled": False,"fill": "white"}).encode(
            y = alt.Y("Temperature:Q", scale = alt.Scale(domain=(df_line["Temperature"].min()-0.5,df_line["Temperature"].max()+0.5))),
            x = alt.X("Time:T", axis=alt.Axis(format="%H:%M"), timeUnit='hoursminutes'))
        chart2 = alt.Chart(df_line).mark_line(point={"filled": False,"fill": "white"}).encode(
            y = alt.Y("Moisture", scale = alt.Scale(domain=(df_line["Moisture"].min()-1.0,df_line["Moisture"].max()+1.0))),
            x = alt.X("Time:T", axis=alt.Axis(format="%H:%M"), timeUnit='hoursminutes'))
        chart3 = alt.Chart(df_line).mark_line(point={"filled": False,"fill": "white"}).encode(
            y = alt.Y("Light", scale = alt.Scale(domain=(df_line["Light"].min()-1.0,df_line["Light"].max()+1.0))),
            x = alt.X("Time:T", axis=alt.Axis(format="%H:%M"), timeUnit='hoursminutes'))    
        chart4 = alt.Chart(df_line).mark_line(point={"filled": False,"fill": "white"}).encode(
            y = alt.Y("Conductivity", scale = alt.Scale(domain=(df_line["Conductivity"].min()-1.0,df_line["Conductivity"].max()+1.0))),
            x = alt.X("Time:T", axis=alt.Axis(format="%H:%M"), timeUnit='hoursminutes')) 

        col1.altair_chart(chart1,use_container_width=True,theme="streamlit")
        col2.altair_chart(chart2,use_container_width=True,theme="streamlit")
        col3.altair_chart(chart3,use_container_width=True,theme="streamlit")
        col4.altair_chart(chart4,use_container_width=True,theme="streamlit")

    def show_line_all_data(self):
        df_line = self.df

        col1, col2, col3, col4 = st.columns(4)

        chart1 = alt.Chart(df_line).mark_line(point={"filled": False,"fill": "white"}).encode(
            y = alt.Y("Temperature", scale = alt.Scale(domain=(df_line["Temperature"].min()-0.5,df_line["Temperature"].max()+0.5)), aggregate="mean"),
            x = alt.X("Time", axis=alt.Axis(format="%d.%m"), timeUnit='monthdate'))
        chart2 = alt.Chart(df_line).mark_line(point={"filled": False,"fill": "white"}).encode(
            y = alt.Y("Moisture", scale = alt.Scale(domain=(df_line["Moisture"].min()-1.0,df_line["Moisture"].max()+1.0)), aggregate="mean"),
            x = alt.X("Time", axis=alt.Axis(format="%d.%m"), timeUnit='monthdate'))
        chart3 = alt.Chart(df_line).mark_line(point={"filled": False,"fill": "white"}).encode(
            y = alt.Y("Light", scale = alt.Scale(domain=(df_line["Light"].min()-1.0,df_line["Light"].max()+1.0)), aggregate="mean"),
            x = alt.X("Time", axis=alt.Axis(format="%d.%m"), timeUnit='monthdate'))    
        chart4 = alt.Chart(df_line).mark_line(point={"filled": False,"fill": "white"}).encode(
            y = alt.Y("Conductivity", scale = alt.Scale(domain=(df_line["Conductivity"].min()-1.0,df_line["Conductivity"].max()+1.0)), aggregate="mean"),
            x = alt.X("Time", axis=alt.Axis(format="%d.%m"), timeUnit='monthdate')) 

        col1.altair_chart(chart1,use_container_width=True,theme="streamlit")
        col2.altair_chart(chart2,use_container_width=True,theme="streamlit")
        col3.altair_chart(chart3,use_container_width=True,theme="streamlit")
        col4.altair_chart(chart4,use_container_width=True,theme="streamlit")

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

option = st.selectbox(
    "Show Data per:",
    ("Hour","Day")
)

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

match option:
    case "Hour":
        sd.show_line()
    case "Day":
        sd.show_line_all_data()



