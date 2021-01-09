import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import time
import timeit

#read Yahoo codes from file
companies = pd.read_csv('Yahoo_Company_codes.csv', names=['yahoocd', 'Description'],skiprows=1)

# Dropping Description column is all values are null
if companies.Description.notnull().sum() == 0: companies.drop('Description', axis=1, inplace=True)

#long string of all yahoo codes as they can be processed at once 
yahoo_tickers = yf.Tickers(' '.join([x for x in companies.yahoocd.values]))


#function to calculate volume ratio 
def get_latest_volume_ratio(yahoo_ticker, period='1mo'):
    ticker_last_X_days = yahoo_ticker.history(period=period)[['Close','Volume']]
    volumes = np.array(ticker_last_X_days.Volume[-2:])
    return float(volumes[-1] / volumes[-2]), max(ticker_last_X_days.index)


#return a df for alll yahoo codes  
def get_table(volume_ratio_cutoff, df = companies):
    rsi_volume = pd.DataFrame([get_latest_volume_ratio(ticker) for ticker in yahoo_tickers.tickers], columns=['vol_ratio','ratio_date']).reindex(df.index)
    df = pd.concat([df, rsi_volume],axis=1 )
    df['action'] = df.vol_ratio.apply(lambda x: 'BUY/SELL' if x > volume_ratio_cutoff else np.nan)
    df = df[df.vol_ratio > volume_ratio_cutoff ]
    return df

# #for testing this code should be commented before importing
# if __name__ == '__main__':
#     timea = time.time()
#     print(get_table(1))
#     print(f'Total Time taken : {time.time()-timea}')    