import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

class Plant_sensor:

    def __init__(self):
        self.df = pd.DataFrame(
            columns=["Datum","Temperatur","Feuchtigkeit","Licht","Leitfähigkeit"]
        )

    def add_entry(self, datum, temp, feuchtigkeit, licht, leitfaehigkeit):
        new_row = [datum,temp,feuchtigkeit,licht,leitfaehigkeit]
        self.df.loc[len(self.df)] = new_row

    def show(self):
        st.write(self.df)

st.write("Hello *World!* :sunglasses:")

ps = Plant_sensor()

date = datetime.now().strftime("%c")
temperatur = str(22)
feuchtigkeit = str(18)
licht = str(5)
leitfaehigkeit = str(50)

ps.add_entry(date,temperatur,feuchtigkeit,licht,leitfaehigkeit)
ps.show()

