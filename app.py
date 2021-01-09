from calculator import get_table
from outlook_mail import send_mail
from datetime import datetime
import pytz
from sql_functions import  insert_df, read_sql_db, delete_table

column_names = ['yahoocd','vol_ratio', 'ratio_date', 'action','query_time']
column_dtypes = ['text','float','time','text','time']

IST = pytz.timezone('Asia/Kolkata')

def checking():
    if int(datetime.now(IST).strftime('%H')) < 9:
        delete_table('high_volume_stocks')
    else:
        df = get_table(3)
        df['query_time'] = datetime.now(IST).strftime('%H:%M:%S')
        insert_df(df,'high_volume_stocks',column_names = column_names, column_dtypes = column_dtypes)
        sql_df = read_sql_db('high_volume_stocks',column_names=column_names)
        print(df, sql_df)
        if len(sql_df):
            send_mail(sql_df)


if __name__ == '__main__':
    checking()
    # print(datetime.now(IST).strftime('%H'))


