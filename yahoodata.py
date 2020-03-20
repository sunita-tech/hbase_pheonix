# this program generates data from yahoo. that you can used for demo in pheonix

import requests
import pandas as pd
import arrow
import datetime
def get_quote_data(symbol='CLDR', data_range='1d', data_interval='1m'):
    res = requests.get('https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={data_range}&interval={data_interval}'.format(**locals()))
    data = res.json()
    #print data
    body = data['chart']['result'][0]
    #print body
    dt = datetime.datetime
    dt = pd.Series(map(lambda x: arrow.get(x).to('US/Pacific').datetime.replace(tzinfo=None), body['timestamp']), name='Datetime')
    df = pd.DataFrame(body['indicators']['quote'][0], index=dt)
    dg = pd.DataFrame(body['timestamp'])
    df = df.loc[:, ('open', 'high', 'low', 'close', 'volume')]
    df.dropna(inplace=True)     #removing NaN rows
    df.columns = ['OPEN', 'HIGH','LOW','CLOSE','VOLUME']    #Renaming columns in pandas
    return df
data = get_quote_data('CLDR', '1d', '1m')
print(data.to_csv())
