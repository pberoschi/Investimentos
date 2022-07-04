# Busca com MACD

from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import pandas as pd 
import time
import telepot
pd.options.mode.chained_assignment = None  # default='warn'

client = Client('jogobafi@gmail.com', 'Johnny321@')

#Selecionando ATIVOS com base em critério de volume
tickers = client.get_ticker()
tabela = pd.DataFrame(tickers)

#Listar em ordem DECRESCENTE
#tabela = tabela.sort_values(by=['lastPrice'], ascending=False)
tabela = tabela.sort_values(by=['volume'], ascending=False)

#Extrair apenas o nome do Ativo
ativosList = list(tabela['symbol'])

#Criando uma lista com 20 ativos
ativos = []
for ativo in ativosList:
    if ativo[-1] == 'T':
        ativos.append(ativo)        
        ativos = ativos[:50]

for ativo in ativos:
    print(ativo)
    resumo4 = client.get_klines(symbol = ativo, interval = client.KLINE_INTERVAL_1HOUR)
    #resumo4 = client.get_klines(symbol = ativo, interval = client.KLINE_INTERVAL_5MINUTE)
    resumo5 = pd.DataFrame(resumo4, columns=['date','open','high','low','close','volume','close_time','asset_volume','n of trades','asset_column','taker_buy','based_asset_volume'])
    resumo6 = resumo5[['date','open','high','low','close','volume','n of trades']]
    resumo6.set_index('date', inplace=True)
    resumo6.index = pd.to_datetime(resumo6.index, unit='ms')


    # MÉDIAS DE 200, 50 e 21
    resumo6['MA200'] = resumo6.close.ewm(span=200).mean()
    resumo6['MA50'] = resumo6.close.ewm(span=50).mean()
    resumo6['MA21'] = resumo6.close.ewm(span=21).mean()

    # MACD
    resumo6['EMA12'] = resumo6.close.ewm(span=12).mean()
    resumo6['EMA26'] = resumo6.close.ewm(span=26).mean()
    resumo6['MACD'] = resumo6.EMA12 - resumo6.EMA26
    resumo6['signal'] = resumo6.MACD.ewm(span=9, adjust=False, min_periods=9).mean()
    resumo6['histog'] = resumo6['MACD'] - resumo6['signal']

    #display(resumo6.tail(2))
    if (resumo6['MA21'].iloc[-2] > resumo6['MA50'].iloc[-2]) & (resumo6['MA50'].iloc[-2] > resumo6['MA200'].iloc[-2]) & ((resumo6['histog'].iloc[-2] > 0) & (resumo6['histog'].iloc[-3] < 0)):
        print(f'{ativo}: Compra')
        bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
        bot.sendMessage(-351556985, f'COMPRA:..........{ativo}')

    if (resumo6['MA21'].iloc[-2] < resumo6['MA50'].iloc[-2]) & (resumo6['MA50'].iloc[-2] < resumo6['MA200'].iloc[-2]) & ((resumo6['histog'].iloc[-2] < 0) & (resumo6['histog'].iloc[-3] > 0)):
        print(f'{ativo}: Venda')
        bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
        bot.sendMessage(-351556985, f'VENDA:..........{ativo}')      