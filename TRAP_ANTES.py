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
    symbols = ['WDOH22','WING22']
    
    for symbol in symbols:
        print(symbol)
        rates10 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M10, 0, 800)
        rates_frame10 = pd.DataFrame(rates10)
        rates_frame10['time']=pd.to_datetime(rates_frame10['time'], unit='s')
        resumo10 = rates_frame10[['time','open','high','low','close','tick_volume']]
        resumo10R = resumo10.tail(4)
        #print(resumo10.head(3))
        #print('')

        rates1 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 780)
        rates_frame1 = pd.DataFrame(rates1)
        rates_frame1['time']=pd.to_datetime(rates_frame1['time'], unit='s')
        resumo1 = rates_frame1[['time','open','high','low','close','tick_volume']]
        resumo1R = resumo1.tail(4)
        #print(resumo1.head(3))
        df1 = resumo1R
        df3 = resumo10R
        result = df1.append(df3)

        OitentaMME = resumo10['close'].ewm(span=80).mean()
        OitoMME = resumo10['close'].ewm(span=8).mean()

        result.insert(loc=6,column='MME 8',value=OitoMME)
        result.insert(loc=7,column='MME 80',value=OitentaMME)

        result['sinal'] = ''
        
        if (result['high'].iloc[-3] < result['high'].iloc[-2]) & (result['close'].iloc[-5] < result['high'].iloc[-2]):
            if result['MME 8'].iloc[-1] < result['MME 80'].iloc[-1]:
                result['sinal'].iloc[-1] = f'VENDA ({symbol})'
                bot = telepot.Bot('5026686955:AAHvm0rJOf-_nSCi8sOHYVMhY8zPCBEd73k')
                bot.sendMessage(984798692, f'TRAP VENDA >> {symbol} <<')
            else:
                result['sinal'].iloc[-1] = 'VENDA: NAM' #NÃO ATENDE MÉDIA

        elif (result['low'].iloc[-3] > result['low'].iloc[-2]) & (result['close'].iloc[-5] > result['low'].iloc[-2]):
            if result['MME 8'].iloc[-1] > result['MME 80'].iloc[-1]:
                result['sinal'].iloc[-1] = f'COMPRA ({symbol})'
                bot = telepot.Bot('5026686955:AAHvm0rJOf-_nSCi8sOHYVMhY8zPCBEd73k')
                bot.sendMessage(984798692, f'TRAP COMPRA >> {symbol} <<')  
            else:
                result['sinal'].iloc[-1] = 'COMPRA NAM' #NÃO ATENDE MÉDIA

        elif (result['high'].iloc[-3] > result['high'].iloc[-2]) & (result['low'].iloc[-3] < result['low'].iloc[-2]):
            tempo = result['time'].iloc[-1]
            result['sinal'].iloc[-1] = f'INSIDE ({symbol})'
            bot = telepot.Bot('5026686955:AAHvm0rJOf-_nSCi8sOHYVMhY8zPCBEd73k')
            bot.sendMessage(984798692, f'>> INSIDE BAR NO {symbol}! TIMEFRAME: 10M ({tempo}) <<')

        else:
            result['sinal'].iloc[-1] = f'MONITORANDO...{symbol})'

        print(result.tail(10))

while True:
    run()
    time.sleep(300)