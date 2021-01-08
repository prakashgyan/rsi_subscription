from calculator import get_table
from outlook_mail import send_mail
from datetime import datetime
import pytz
from sql_functions import create_table, insert_df, read_sql_db, delete_table
column_names = ['YahooCD','Vol_Ratio','VR_Purchase']
column_dtypes = ['text','float','text']

IST = pytz.timezone('Asia/Kolkata')

def checking():
    if int(datetime.now(IST).strftime('%H')) < 9:
        delete_table('stocks')
    else:
        df,run_time = get_table(3)
        # create_table('stocks',['S_No','YahooCD','Vol_Ratio','VR_Purchase'],['NUMERIC','text','float','text'])
        insert_df(df,'stocks')
        sql_df = read_sql_db('stocks',column_names)
        print(df, sql_df)
        if len(sql_df):
            send_mail(sql_df)


if __name__ == '__main__':
    checking()
    print(datetime.now(IST).strftime('%H'))


