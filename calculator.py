import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import time
import timeit


companies = pd.read_csv('Yahoo_Company_codes.csv')
# Dropping Description column is all values are null
if companies.Description.notnull().sum() == 0: companies.drop('Description', axis=1, inplace=True)

"""Rules for Calculation"""
# period = '1mo'  # time frame of data to get for calculation of RSI
# RSI_buy_sell = [25, 75]  # SELL if less than 25 buy when more than 75
# VOL_RATIO_buy_sell = 3  # BUY/SELL when volume ratio is more than 3
# timeofevent = datetime.now().strftime("%c")

yahoo_tickers = yf.Tickers(' '.join([x for x in companies.YahooCD.values]))

def get_current_rsi(yahoo_ticker, period='12mo'):
    # yahoo_ticker = yf.Ticker(comp_cd)
    ticker_last_X_days = yahoo_ticker.history(period=period)[['Close','Volume']]
    # ticker_last_X_days['Change'] = ticker_last_X_days.Close.rolling(2).apply(lambda x: x[-1] - x[0])
    # ticker_last_X_days['Upward_movement'] = ticker_last_X_days.Change.apply(lambda x: x if x > 0 else 0)
    # ticker_last_X_days['Downward_movement'] = ticker_last_X_days.Change.apply(lambda x: -x if x < 0 else 0)
    # up_mean = ticker_last_X_days.Upward_movement[:14].mean()
    # down_mean = ticker_last_X_days.Downward_movement[:14].mean()
    # ticker_last_X_days['Avg_upward_movement'] = None
    # ticker_last_X_days['Avg_downward_movement'] = None
    # avg_mov_updater(ticker_last_X_days, up_mean, down_mean)
    # ticker_last_X_days[
    #     'Relative_strength'] = ticker_last_X_days.Avg_upward_movement / ticker_last_X_days.Avg_downward_movement
    # ticker_last_X_days['RSI'] = 100 - 100 / (ticker_last_X_days.Relative_strength + 1)
    volumes = np.array(ticker_last_X_days.Volume[-2:])
    return float(volumes[-1] / volumes[-2])


def avg_mov_updater(df, upavg, downavg):
    new_upavg = upavg
    new_downavg = downavg
    up_to_be_updated = df.Upward_movement[14:]
    down_to_be_updated = df.Downward_movement[14:]
    up_updated = [None] * 13 + [new_upavg]
    down_updated = [None] * 13 + [new_downavg]

    for i, j in zip(up_to_be_updated, down_to_be_updated):
        new_upavg = (new_upavg * 13 + i) / 14
        new_downavg = (new_downavg * 13 + j) / 14
        up_updated.append(new_upavg)
        down_updated.append(new_downavg)

    df['Avg_upward_movement'] = up_updated
    df['Avg_downward_movement'] = down_updated



def get_table(VOL_RATIO_buy_sell, df = companies):
    # try:    
    # RSI_buy_sell = [int(x) for x in form_data['rsi_buy_sell'].split(',') ]
    # VOL_RATIO_buy_sell = int(form_data['vol_ratio_trigger'])
    # period = form_data['period']
    rsi_volume = pd.DataFrame([get_current_rsi(ticker) for ticker in yahoo_tickers.tickers], columns=['Vol_Ratio']).reindex(df.index)
    df = pd.concat([df, rsi_volume],axis=1 )
    # df['RSI'] = df.YahooCD.apply(get_current_rsi)
    # # companies['beta'] = companies.YahooCD.apply(get_beta)
    # df['Buy/Sell'] = df.RSI.apply(
    #     lambda x: 'BUY' if x < RSI_buy_sell[0] else ('SELL' if x > RSI_buy_sell[1] else np.nan))
    # df['vol_Ratio'] = df.YahooCD.apply(volume)
    # df = df[['YahooCD','RSI','Buy/Sell','Vol_Ratio']]
    df['VR Purchase'] = df.Vol_Ratio.apply(lambda x: 'BUY/SELL' if x > VOL_RATIO_buy_sell else np.nan)
    # # companies.to_json('data_json.json')
    df = df[df.Vol_Ratio > VOL_RATIO_buy_sell ]
    timeofevent = datetime.utcnow() + timedelta(hours=5,minutes=30)
    return df , f'[IST] {timeofevent.strftime("%c")}'

# if __name__ == '__main__':
#     timea = time.time()
#     print(get_table(3))
#     # print(yf.Ticker('POWERGRID.NS').history('1mo'))
#     print(f'Total Time taken : {time.time()-timea}')    