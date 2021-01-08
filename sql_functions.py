import sqlite3
import pandas as pd


def create_table(table_name , column_names , data_types):
    conn= sqlite3.connect('stcoks.db')
    c = conn.cursor()
    table_metadata = ', '.join([ ' '.join([x,y]) for x,y in zip(column_names,data_types)])
    sql_commmand = f"CREATE TABLE IF NOT EXISTS {table_name} ({table_metadata})"
    print(sql_commmand)
    c.execute(sql_commmand)
    conn.commit()
    conn.close()

def insert_df(df,table_name,append_replace = 'append'):
    conn= sqlite3.connect('stcoks.db')
    # c = conn.cursor()
    df.to_sql(table_name,conn,if_exists=append_replace, index = False)
    conn.commit()
    conn.close()

def read_sql_db(table_name,column_names):
    conn= sqlite3.connect('stcoks.db')
    c = conn.cursor()
    c.execute(f"select * from {table_name} ")
    return pd.DataFrame(c.fetchall(),columns=column_names)

def delete_table(table_name):
    conn= sqlite3.connect('stcoks.db')
    c = conn.cursor()
    c.execute(f'DROP TABLE IF EXISTS {table_name}')
    print('table_deleted')
    conn.commit()
    conn.close()



# c.execute('''CREATE TABLE stocks
#              (date text, YahooCD text, Vol_ratio float, VR_purchage text)''')

# c.execute("INSERT INTO stocks VALUES ('2006-01-05','BAJFINANCE.NS',0.737843,'nan')")
# c.execute("select * from stocks")
# print(c.fetchall())
# conn.commit()
# conn.close()