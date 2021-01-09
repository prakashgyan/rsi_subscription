import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text
DATABASE_URL = os.environ['DATABASE_URL']

table_name = 'high_volume_stocks'
engine = create_engine(DATABASE_URL)

# with engine.connect() as conn:
#     # conn.execute('alter table stocks rename column [VR Purchase] to VR_Purchase')
#     conn.execute(text('''CREATE TABLE if not exists Cars(Id INTEGER PRIMARY KEY, 
#                  Name TEXT, Price INTEGER)'''))
#     data = ( { "Id": 9, "Name": "Audi", "Price": 52642 },
#              { "Id": 10, "Name": "Mercedes", "Price": 57127 }
#             #  { "Id": 3, "Name": "Skoda", "Price": 9000 },
#             #  { "Id": 4, "Name": "Volvo", "Price": 29000 },
#             #  { "Id": 5, "Name": "Bentley", "Price": 350000 },
#             #  { "Id": 6, "Name": "Citroen", "Price": 21000 },
#             #  { "Id": 7, "Name": "Hummer", "Price": 41400 },
#             #  { "Id": 8, "Name": "Volkswagen", "Price": 21600 }
#     )
#     for line in data:
#         conn.execute(text("""INSERT INTO Cars(Id, Name, Price) 
#                 VALUES(:Id, :Name, :Price)"""), **line)

# with engine.connect() as conn:
#     # conn.execute('alter table stocks rename column [VR Purchase] to VR_Purchase')
#     result = conn.execute(text('''select name, max(price) from cars group by Name having count(*) =1'''))
#     print(pd.DataFrame(result))

with engine.connect() as conn:
# conn.execute('alter table stocks rename column [VR Purchase] to VR_Purchase')
    conn.execute(text(f'drop table {table_name}'))
    result = conn.execute(text(f'''select yahoocd, max(vol_ratio), max(action), max(time) 
                                    from high_volume_stocks group by yahoocd having count(*) =1 '''))
    print(pd.DataFrame(result))
    # conn.execute(text('Create table if not exists high_volume_stocks (yahoocd Text, vol_ratio float, action Text, time time) '))
    