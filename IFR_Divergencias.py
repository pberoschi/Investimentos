from datetime import datetime
import MetaTrader5 as mt5
import time
import telepot
import pytz
import numpy as np

# importamos o módulo pandas para exibir os dados recebidos na forma de uma tabela
import pandas as pd
pd.set_option('display.max_columns', 500) # número de colunas
pd.set_option('display.width', 1500)      # largura máxima da tabela
pd.options.mode.chained_assignment = None  # default='warn'

if not mt5.initialize(login=1092947504, server="ClearInvestimentos-DEMO", password="Joh0516"):
#if not mt5.initialize(login=4999473749, server="MetaQuotes-Demo", password="elf4lnbx"):
    print("initialize() failed, error code =",mt5.last_error())
    quit()
    
#symbols = ['EURUSD','GBPUSD','USDCAD','USDJPY', 'USDCHF','AUDUSD','NZDUSD']
symbols = ['WDON22','WINM22']

def rodar():
    for symbol in symbols:
        print(symbol)
        rates10 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 0, 800)
        rates_frame10 = pd.DataFrame(rates10)
        rates_frame10['time']=pd.to_datetime(rates_frame10['time'], unit='s')
        resumo = rates_frame10[['time','open','high','low','close','tick_volume']]
        resumo1 = resumo[['time','high','low']]
        #print(resumo.tail())
        #print('')

        maximas = (resumo1[['high']].tail(3))
        high1 = resumo1['high'].iloc[-2]
        high2 = resumo1['high'].iloc[-3]

        minimas = (resumo1[['low']].tail(3))
        low1 = resumo1['low'].iloc[-2]
        low2 = resumo1['low'].iloc[-3]

        resumo1.insert(loc=3,column='H1',value=high1)
        resumo1.insert(loc=4,column='H2',value=high2)

        resumo1.insert(loc=5,column='L1',value=low1)
        resumo1.insert(loc=6,column='L2',value=low2)

        #resumo1 = resumo1.tail(1)
        #display(resumo1)


        # >>> CALCULO RSI IFR <<<
        delta = resumo['close'].diff()
        up = delta.clip(lower=0)
        down = -1*delta.clip(upper=0)
        ema_up = up.ewm(com=8, adjust=False).mean()
        ema_down = down.ewm(com=8, adjust=False).mean()
        rs = ema_up/ema_down
        RSI1 = (100 - (100/(1 + rs)).iloc[-2])
        RSI2 = (100 - (100/(1 + rs)).iloc[-3])

        resumo1.insert(loc=7,column='RSI1',value=RSI1)
        resumo1.insert(loc=8,column='RSI2',value=RSI2)


        # ORGANIZANDO DADOS NA TABELA #
        resumo1['ALTA'] = ''
        resumo1['BAIXA'] = ''
        resumo1['Div BAIXA'] = ''
        resumo1['Div ALTA'] = ''


        DivBaixa = (resumo1['H1'].iloc[-1] > resumo1['H2'].iloc[-1]) & (resumo1['RSI1'].iloc[-1] < resumo1['RSI2'].iloc[-1])
        DivAlta = (resumo1['L1'].iloc[-1] < resumo1['L2'].iloc[-1]) & (resumo1['RSI1'].iloc[-1] > resumo1['RSI2'].iloc[-1])

        #DivBaixa is True
        #DivAlta is True
        
        if resumo1['H1'].iloc[-1] > resumo1['H2'].iloc[-1]:
            resumo1['ALTA'].iloc[-1] = 'ALTA'
        else:
            resumo1['ALTA'] = ''

        if resumo1['L1'].iloc[-1] < resumo1['L2'].iloc[-1]:
            resumo1['BAIXA'].iloc[-1] = 'BAIXA'
        else:
            resumo1['BAIXA'] = ''
            
        if (resumo1['H1'].iloc[-1] > resumo1['H2'].iloc[-1]) & (resumo1['RSI1'].iloc[-1] < resumo1['RSI2'].iloc[-1]): 
            resumo1['Div BAIXA'].iloc[-1] = 'DIV BAIXA'
            #MENSAGEM NA MUDANÇA DE CONDICAO
            bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
            bot.sendMessage(-351556985, f'DIVERGÊNCIA DE BAIXA: {symbol}')
        else:
            resumo1['Div BAIXA'].iloc[-1] = ''
            
        if (resumo1['L1'].iloc[-1] < resumo1['L2'].iloc[-1]) & (resumo1['RSI1'].iloc[-1] > resumo1['RSI2'].iloc[-1]):
            resumo1['Div ALTA'].iloc[-1] = 'DIV ALTA'
            
        else:
            resumo1['Div ALTA'].iloc[-1] = ''    
            
                
        print(resumo1.tail(1))

while True:
    rodar()
    time.sleep(900)