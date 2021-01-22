import os
# Outlook 
MY_ADDRESS = os.environ["MY_EMAIL_ADDRESS"]
PASSWORD = os.environ["MY_EMAIL_PASSWORD"]

#database
DATABASE_URL = os.environ['DATABASE_URL']

#app
weekends = ['Saturday', 'Sunday']
column_names = ['yahoocd','vol_ratio', 'ratio_date', 'action','query_time']
column_dtypes = ['text','float','date','text','time']