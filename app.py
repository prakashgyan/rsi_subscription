from calculator import get_table
from outlook_mail import send_mail
from datetime import datetime
import pytz
from sql_functions import  insert_df, read_sql_db, delete_table
from metadata import *


IST = pytz.timezone('Asia/Kolkata')

def checking():
    if datetime.now(IST).strftime('%A') in weekends: return 0
    if int(datetime.now(IST).strftime('%H')) < 9:
        delete_table('high_volume_stocks')
    else:
        df, max_ratio_date = get_table(3)
        if max_ratio_date == datetime.now(IST).strftime(r'%Y-%m-%d'): 
            df['query_time'] = datetime.now(IST).strftime('%H:%M:%S')
            insert_df(df,'high_volume_stocks',column_names = column_names, column_dtypes = column_dtypes)
            sql_df = read_sql_db('high_volume_stocks',column_names=column_names)
            print(df, sql_df)
            if len(sql_df):
                send_mail(sql_df)


if __name__ == '__main__':
    checking()
    # print(datetime.now(IST).strftime('%H'))


