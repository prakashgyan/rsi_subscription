from calculator import get_table
from outlook_mail import send_mail
from datetime import datetime
import pytz
from sql_functions import insert_df, sql_query, delete_table, create_table, sql_execute_query, truncate_table
from metadata import *

IST = pytz.timezone('Asia/Kolkata')


def checking():
    if datetime.now(IST).strftime('%A') in weekends: return 0
    if int(datetime.now(IST).strftime('%H')) < 9:
        delete_table('sent_data')

    else:
        df, max_ratio_date = get_table(3)
        if max_ratio_date == datetime.now(IST).strftime(r'%Y-%m-%d'):
            df['query_time'] = datetime.now(IST).strftime('%H:%M:%S')
            truncate_table('high_volume_stocks')
            insert_df(df, 'high_volume_stocks', column_names=column_names, column_dtypes=column_dtypes)
            email_df = sql_execute_query(sql_query,column_names=column_names[:-1])
            email_df['query_time'] = datetime.now(IST).strftime('%H:%M:%S')
            print(df, email_df)
            try :               
                if len(email_df):
                    send_mail(email_df)
                    insert_df(email_df, 'sent_data', column_names=column_names, column_dtypes=column_dtypes)
            except:
                print("Error sending Email and Db is not updated")




if __name__ == '__main__':
    checking()
    # print(datetime.now(IST).strftime('%H'))
