from datetime import datetime
import MetaTrader5 as mt5
import time
import telepot
import pytz

# importamos o módulo pandas para exibir os dados recebidos na forma de uma tabela
import pandas as pd
pd.set_option('display.max_columns', 500) # número de colunas
pd.set_option('display.width', 1500)      # largura máxima da tabela
pd.options.mode.chained_assignment = None  # default='warn'

if not mt5.initialize(login=1092947504, server="ClearInvestimentos-DEMO", password="Joh0516"):
#if not mt5.initialize(login=4999473749, server="MetaQuotes-Demo", password="elf4lnbx"):
    print("initialize() failed, error code =",mt5.last_error())
    quit()
   

def run():
    #symbols = ['EURUSD','USDJPY']
    symbols = ['WDOG22','WING22']
    
    for symbol in symbols:
        print(symbol)
        rates10 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 0,300)
        rates_frame10 = pd.DataFrame(rates10)
        rates_frame10['time']=pd.to_datetime(rates_frame10['time'], unit='s')
        resumo10 = rates_frame10[['time','open','high','low','close','tick_volume']]
        resumo10R = resumo10
        result = resumo10R
        #print(resumo10.head(3))
        #print('')

        OitentaMME = resumo10['close'].ewm(span=80).mean()
        OitoMME = resumo10['close'].ewm(span=8).mean()

        resumo10.insert(loc=6,column='MME 8',value=OitoMME)
        resumo10.insert(loc=7,column='MME 80',value=OitentaMME)

        #resumo10.tail()

        resumo10['sinal'] = ''        

        if (resumo10['high'].iloc[-4] < resumo10['high'].iloc[-3]) & (resumo10['high'].iloc[-3] > resumo10['high'].iloc[-2]) & (resumo10['low'].iloc[-3] > resumo10['low'].iloc[-2]):
            if resumo10['MME 8'].iloc[-1] < resumo10['MME 80'].iloc[-1]:
                resumo10['sinal'].iloc[-1] = f'VENDA ({symbol})'
                bot = telepot.Bot('5026686955:AAHvm0rJOf-_nSCi8sOHYVMhY8zPCBEd73k')
                bot.sendMessage(984798692, f'ESTRATÉGIA TRAP: VENDA >> {symbol} <<')

        elif (resumo10['low'].iloc[-4] > resumo10['low'].iloc[-3]) & (resumo10['low'].iloc[-3] < resumo10['low'].iloc[-2]) & (resumo10['high'].iloc[-3] < resumo10['high'].iloc[-2]):
            if resumo10['MME 8'].iloc[-1] > resumo10['MME 80'].iloc[-1]:
                resumo10['sinal'].iloc[-1] = f'COMPRA ({symbol})'
                bot = telepot.Bot('5026686955:AAHvm0rJOf-_nSCi8sOHYVMhY8zPCBEd73k')
                bot.sendMessage(984798692, f'ESTRATÉGIA TRAP: COMPRA >> {symbol} <<')

        else:
            result['sinal'].iloc[-1] = f'MONITORANDO...{symbol})'

        print(result.tail(4))

    
while True:
    run()
    time.sleep(900)