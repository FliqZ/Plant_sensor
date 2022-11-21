import gspread
import pandas as pd
from datetime import datetime, timedelta

gc = gspread.service_account()

sheet = gc.open_by_key('1SIVicNq5FcrDpr73jNOlQ6vsvpBnSpLvm0LcGY-FGzQ')

worksheet = sheet.get_worksheet(0)

#entry1
date = datetime.now() + timedelta(hours=0.1)
date = date.strftime("%c")
temperatur = str(23)
feuchtigkeit = str(47)
licht = str(44)
leitfaehigkeit = str(31)
data = {"Datum":[date],
            "Temperatur":[temperatur],
            "Feuchtigkeit":[feuchtigkeit],
            "Licht":[licht],
            "Leitfähigkeit":[leitfaehigkeit]
            }

df = pd.DataFrame(data)
params = {'valueInputOption': 'USER_ENTERED'}
body = {'values': df.values.tolist()}
sheet.values_append(f"Data!A2",params,body)
#worksheet.append_row([df.columns.values.tolist()] + df.values.tolist(),)
