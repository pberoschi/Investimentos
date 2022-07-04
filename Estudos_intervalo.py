from datetime import datetime
import MetaTrader5 as mt5
import time
import telepot
import pytz

agora = datetime.now()
print(f'Buscando dados...{agora}')
# importamos o módulo pandas para exibir os dados recebidos na forma de uma tabela
import pandas as pd
pd.set_option('display.max_columns', 500) # número de colunas
pd.set_option('display.width', 1500)      # largura máxima da tabela
pd.options.mode.chained_assignment = None  # default='warn'


if not mt5.initialize(login=54679378, server="MetaQuotes-Demo", password="hz7ulfri"):
    print("initialize() failed, error code =",mt5.last_error())
    quit()

# CRIAÇÃO DAS ORDENS ABERTURA E FECHAMENTO

# linhas (81;115;205)
symbol = "USDCNH"
item = symbol
ativo = symbol

print(symbol)


# CRIAÇÃO DOS CÁLCULOS (MÉDIAS)
# definimos o fuso horário como UTC
timezone = pytz.timezone("Etc/UTC")
# criamos o objeto datetime no fuso horário UTC para que não seja aplicado o deslocamento do fuso horário local
utc_from = datetime(2021, 12, 10, tzinfo=timezone)
# recebemos 10 barras de EURUSD H4 a partir de 01/10/2019 no fuso horário UTC
rates = mt5.copy_rates_from(item, mt5.TIMEFRAME_M5, utc_from, 113)
# a partir dos dados recebidos criamos o DataFrame
rates_frame = pd.DataFrame(rates)
# convertemos o tempo em segundos no formato datetime
rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
resumo = rates_frame[['time','open','close','spread']]
#resumo

# SETUP 30.3
TrintaMME = resumo['close'].ewm(span=30).mean() 
TresMME = resumo['close'].ewm(span=3).mean()

resumo.insert(loc=4,column='MME 30',value=TrintaMME)
resumo.insert(loc=5,column='MME 3',value=TresMME)


# MACD
resumo['EMA12'] = resumo.close.ewm(span=12).mean()
resumo['EMA26'] = resumo.close.ewm(span=26).mean()
resumo['MACD'] = resumo.EMA12 - resumo.EMA26
resumo['signal'] = resumo.MACD.ewm(span=9).mean()
resumo['histog'] = resumo['MACD'] - resumo['signal']
#display(resumo.tail(60))

#teste = resumo[['MACD','signal','histog']]
#display(teste.tail(60))


# MONITORAMENTO
resumo['flag'] = ''
resumo['sinal'] = ''

for i in range (1, len(resumo)):
    if resumo['MME 30'][i] < resumo['MME 3'][i]:
        resumo['flag'][i] = 'COMPRA'
    else:
        resumo['flag'][i] = 'VENDA'

for x in range(1,len(resumo)):
    if resumo['flag'][x] == resumo['flag'][x-1]:
        resumo['sinal'][x] = ''
    else:
        resumo['sinal'][x] = 'sinal'

resumo_resumo = resumo[['time','open','close','MACD','signal','histog']]
#resumo_resumo

filtro = resumo_resumo.loc[resumo_resumo["time"].between('2021-12-09 11:25:00', '2021-12-09 11:50:00')]
print(filtro)