import sqlite3
import pandas as pd


conn= sqlite3.connect('stcoks.db')
c = conn.cursor()
c.execute(f"select YahooCD, Vol_Ratio, [VR Purchase], Time from stocks group by YahooCD having count(yahooCD) = 5")
print(pd.DataFrame(c.fetchall()))