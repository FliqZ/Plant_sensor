import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class Plant_sensor:

    def __init__(self):
        self.df = pd.DataFrame(
            columns=["Datum","Temperatur","Feuchtigkeit","Licht","Leitfähigkeit"]
        )

    def add_entry(self, datum, temp, feuchtigkeit, licht, leitfaehigkeit):
        new_row = [datum,temp,feuchtigkeit,licht,leitfaehigkeit]
        self.df.loc[len(self.df)] = new_row

    def show_table(self):
        st.write(self.df)

    def show_line(self, x):
        st.line_chart(self.df, x = x)

st.title("Pflanzensensor Datenauswertung")

ps = Plant_sensor()

#entry1
date = datetime.now().strftime("%c")
temperatur = str(22)
feuchtigkeit = str(18)
licht = str(5)
leitfaehigkeit = str(50)
#entry2
date2 = datetime.now() - timedelta(hours=1)
date2 = date2.strftime("%c")
temperatur2 = str(20)
feuchtigkeit2 = str(18)
licht2 = str(6)
leitfaehigkeit2 = str(65)
#entry3
date3 = datetime.now() - timedelta(hours=2)
date3 = date3.strftime("%c")
temperatur3 = str(18)
feuchtigkeit3 = str(18)
licht3 = str(7)
leitfaehigkeit3 = str(70)

ps.add_entry(date,temperatur,feuchtigkeit,licht,leitfaehigkeit)
ps.add_entry(date2,temperatur2,feuchtigkeit2,licht2,leitfaehigkeit2)
ps.add_entry(date3,temperatur3,feuchtigkeit3,licht3,leitfaehigkeit3)
ps.show_table()
ps.show_line(x="Datum")

