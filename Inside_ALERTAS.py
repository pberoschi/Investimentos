from datetime import datetime
import MetaTrader5 as mt5
import time
import telepot
import pytz

import pandas as pd
pd.set_option('display.max_columns', 500) # número de colunas
pd.set_option('display.width', 1500)      # largura máxima da tabela
pd.options.mode.chained_assignment = None  # default='warn'

agora = datetime.now()
#print(f'Buscando dados...{agora}')

#if not mt5.initialize(login=54679378, server="MetaQuotes-Demo", password="hz7ulfri"):
if not mt5.initialize(login=1092947504, server="ClearInvestimentos-DEMO", password="Joh0516"):
    print("initialize() failed, error code =",mt5.last_error())
    quit()

def run():
    diaHoje = 31
    diaAmanha = diaHoje + 1
    diaHoje = str(diaHoje)

    symbols = ['WDOG22','WING22']
    #symbols = ['EURUSD','USDJPY']

    for symbol in symbols:
        print(symbol)
        # CRIAÇÃO DOS CÁLCULOS (MÉDIAS)
        #timezone = pytz.timezone("Etc/UTC")
        #utc_from = datetime(2022, 1, diaAmanha, tzinfo=timezone)
        ratesM10 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M10, 0, 500)
        rates_frameM10 = pd.DataFrame(ratesM10)
        rates_frameM10['time']=pd.to_datetime(rates_frameM10['time'], unit='s')
        dfM10 = rates_frameM10[['time','open','high','low','close']]
        #dfM15 = dfM15.tail()

        #dfM15 = dfM1.loc[dfM1["time"].between('2022-1-4 10:01:00', '2022-1-4 18:00:00')]
        #dfM15.tail()

        dfM10['INSIDE'] = ''
        #X = 1 # FORCE
        #if X == 1: # FORCE
        
        if (dfM10['high'].iloc[-3] > dfM10['high'].iloc[-2]) & (dfM10['low'].iloc[-3] < dfM10['low'].iloc[-2]):
            tempo = dfM10['time'].iloc[-1]
            dfM10['INSIDE'].iloc[-1] = 'INSIDE'
            # ENVIAR MENSAGEM TELEGRAM
            #bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
            #bot.sendMessage(-766185524, f'>> INSIDE BAR NO {symbol}! TIMEFRAME: 10M ({tempo}) <<')
            bot = telepot.Bot('5026686955:AAHvm0rJOf-_nSCi8sOHYVMhY8zPCBEd73k')
            bot.sendMessage(984798692, f'>> INSIDE BAR NO {symbol}! TIMEFRAME: 10M ({tempo}) <<')
            #else:
                #print('nada a enviar')

        else:
            dfM10['INSIDE'].iloc[-1] = ''

        print(dfM10.tail(5))
        
    print('Fim do processo')


while True:
    run()
    time.sleep(600)

'''
# ESTUDOS: 
# LEVANTAMENTO DE QUANTOS INSIDES OCORRERAM

from datetime import datetime
import MetaTrader5 as mt5
import time
import telepot
import pytz

import pandas as pd
pd.set_option('display.max_columns', 500) # número de colunas
pd.set_option('display.width', 1500)      # largura máxima da tabela
pd.options.mode.chained_assignment = None  # default='warn'

agora = datetime.now()
#print(f'Buscando dados...{agora}')

#if not mt5.initialize(login=54679378, server="MetaQuotes-Demo", password="hz7ulfri"):
if not mt5.initialize(login=1092947504, server="ClearInvestimentos-DEMO", password="Joh0516"):
    print("initialize() failed, error code =",mt5.last_error())
    quit()


symbols = ['WDOG22','WING22']


for symbol in symbols:
    print(symbol)
    ratesM15 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 0, 40)
    rates_frameM15 = pd.DataFrame(ratesM15)
    rates_frameM15['time']=pd.to_datetime(rates_frameM15['time'], unit='s')
    dfM15 = rates_frameM15[['time','open','high','low','close']]
    dfM15['INSIDE'] = ''

    for i in range (5,len(dfM15)):
        if (dfM15['high'][i-3] > dfM15['high'][i-2]) & (dfM15['low'][i-3] < dfM15['low'][i-2]):
            dfM15['INSIDE'][i-1] = 'INSIDE'

        else:
            dfM15['INSIDE'][i] = ''

    display(dfM15)



# ENVIO DE MENSAGENS TELEGRAM
bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
bot.sendMessage(-766185524, f'>> INSIDE NO {symbol}! TIMEFRAME: 15 min <<')


'''