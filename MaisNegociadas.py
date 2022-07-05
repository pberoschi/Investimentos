#from flask.templating import DispatchingJinjaLoader
import pandas as pd
from bs4 import BeautifulSoup
import requests
pd.options.mode.chained_assignment = None

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
url = ('https://br.tradingview.com/markets/stocks-brazilia/market-movers-active/')
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'lxml')
table = soup.find_all('table')[0]
tabela = pd.read_html(str(table),decimal='.')[0]
tabela.rename(columns={'Unnamed: 0': 'TICKER',
                'Unnamed: 1': 'PREÇO',
                'Unnamed: 2': 'VARPorc',
                'Unnamed: 3': 'VAR',
                'Unnamed: 4': 'CLASSIFICAÇÃO',
                'Unnamed: 5': 'VOLUME',
                'Unnamed: 6': 'CAP_MERCADO',
                'Unnamed: 7': 'P_L',
                'Unnamed: 8': 'EPS_12M',
                'Unnamed: 9': 'FUNCIONÁRIOS',
                'Unnamed: 10': 'SETOR'
                }, inplace = True)
resumoMN = tabela.to_dict('records')