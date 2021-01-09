import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text


DATABASE_URL = os.environ['DATABASE_URL']
engine = create_engine(DATABASE_URL)

def create_table(table_name , column_names , data_types):
    with engine.connect() as conn:
        table_metadata = ', '.join([ ' '.join([x,y]) for x,y in zip(column_names,data_types)])
        sql_commmand = f"CREATE TABLE IF NOT EXISTS {table_name} ({table_metadata})"
        print(sql_commmand)
        conn.execute(text(sql_commmand))
        # conn.commit()

def insert_df(df,table_name,column_names,column_dtypes, append_replace = 'append'):
    with engine.connect() as conn:
        # c = conn.cursor()
        # conn.execute(text(f'Create table if not exists {table_name} (yahoocd Text, vol_ratio float, action Text, time time) '))
        create_table(table_name,column_names,column_dtypes)
        df.to_sql(table_name,conn,if_exists=append_replace, index = False)
        # conn.commit()

def read_sql_db(table_name,column_names):
    with engine.connect() as conn:

        # c = conn.cursor()
        result = conn.execute(text(f'''select yahoocd, max(vol_ratio), max(ratio_date), max(action), max(query_time) 
                                    from {table_name} group by yahoocd having count(*) =1 '''))
        return pd.DataFrame(result ,columns=column_names)

def delete_table(table_name):
    with engine.connect() as conn:
        # c = conn.cursor()
        conn.execute(text(f'DROP TABLE IF EXISTS {table_name}'))
        print('table_deleted')
        # conn.commit()
        # conn.close()



# c.execute('''CREATE TABLE stocks
#              (date text, YahooCD text, Vol_ratio float, VR_purchage text)''')

# c.execute("INSERT INTO stocks VALUES ('2006-01-05','BAJFINANCE.NS',0.737843,'nan')")
# c.execute("select * from stocks")
# print(c.fetchall())
# conn.commit()
# conn.close()