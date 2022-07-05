# COM MACD
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


#if not mt5.initialize(login=54679378, server="MetaQuotes-Demo", password="hz7ulfri"):
if not mt5.initialize(login=50717088, server="ICMarketsSC-Demo", password="2DLJdDev"):
    print("initialize() failed, error code =",mt5.last_error())
    quit()

symbol = ["EURUSD","GBPUSD","USDJPY","USDCHF","USDCAD","AUDUSD","NZDUSD"]
#item = "WDOZ21"

for item in symbol:
    print(f'Ativo: {item}')
    timezone = pytz.timezone("Etc/UTC")
    utc_from = datetime(2021, 12, 2, tzinfo=timezone)
    rates = mt5.copy_rates_from(item, mt5.TIMEFRAME_M5, utc_from, 113)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
    resumo = rates_frame[['time','open','close','spread']]
    #resumo

    #Criar Sinais de compra e venda
    openMME = resumo['open'].ewm(span=3).mean()      #cor: VERDE(3)
    closeMME = resumo['close'].ewm(span=30).mean()   #cor: VERMELHA(30)
    resumo.insert(loc=4,column='MMEopen',value=openMME)
    resumo.insert(loc=5,column='MMEclose',value=closeMME)
    #print(resumo.tail())

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
    pd.options.mode.chained_assignment = None
    resumo['flag'] = ''
    resumo['sinal'] = ''

    for i in range (1, len(resumo)):
        if resumo['MMEopen'][i] > resumo['MMEclose'][i]:
            resumo['flag'][i] = 'COMPRA'
        else:
            resumo['flag'][i] = 'VENDA'

    for x in range(1,len(resumo)):
        if resumo['flag'][x] == resumo['flag'][x-1]:
            resumo['sinal'][x] = ''
        else:
            resumo['sinal'][x] = 'sinal'

    flag = resumo['flag'].iloc[-1]

    #resumo['sinal'].iloc[-1] = 'sinal'
    #resumo['flag'].iloc[-1] = 'COMPRA'

    if resumo['sinal'].iloc[-1] == 'sinal':
        bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
        bot.sendMessage(-351556985, f'ATENÇÃO! MUDANÇA DE STATUS: >> {item} - {flag} <<')
        print('Dados encontrados e enviados via Telegram'.upper())


    # AVISO DE SAÍDA DA OPERAÇÃO    
    compraHISTOG = resumo['histog'].iloc[-4] > 0 and resumo['histog'].iloc[-3] > 0 and resumo['histog'].iloc[-2] > 0
    compraSIGNAL = resumo['signal'].iloc[-4] > 0 and resumo['signal'].iloc[-3] > 0 and resumo['signal'].iloc[-2] > 0    
    lucroCOMPRA = compraHISTOG and resumo['histog'].iloc[-1] < 0 and compraSIGNAL and resumo['signal'].iloc[-1] > 0
    resumo['lucroCOMPRA'] = lucroCOMPRA
    #lucroCOMPRA = True

    vendaHISTOG = resumo['histog'].iloc[-4] < 0 and resumo['histog'].iloc[-3] < 0 and resumo['histog'].iloc[-2] < 0
    vendaSIGNAL = resumo['signal'].iloc[-4] < 0 and resumo['signal'].iloc[-3] < 0 and resumo['signal'].iloc[-2] < 0     
    lucroVENDA = compraHISTOG and resumo['histog'].iloc[-1] > 0 and compraSIGNAL and resumo['signal'].iloc[-1] < 0
    resumo['lucroVENDA'] = lucroVENDA
    #lucroVENDA = True

    if lucroCOMPRA == True:
        bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
        bot.sendMessage(-351556985, f'ATENÇÃO! LUCRO MÁXIMO NA COMPRA: >> {item} <<')
        print('Dados encontrados e enviados via Telegram'.upper())

    if lucroVENDA == True:
        bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
        bot.sendMessage(-351556985, f'ATENÇÃO! LUCRO MÁXIMO NA VENDA: >> {item} <<')
        print('Dados encontrados e enviados via Telegram'.upper())


    print(resumo.tail(3))
    time.sleep(3)
    print('')

print('')
print('Script executado com sucesso!'.upper())
#time.sleep()
    