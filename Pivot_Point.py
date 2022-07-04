import MetaTrader5 as mt5
from datetime import datetime
import time
import pandas as pd
from pandas_datareader import data as pdr
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline

ticker = input("Qual o ativo que deseja monitorar? ").upper()
#LETRAS MAIUSCULAS NO ATIVO


# estabelecemos a conexão ao MetaTrader 5; conecte-se ao MetaTrader 5
#if not mt5.initialize(login=1092947504, server="ClearInvestimentos-DEMO", password="Joh0516"):
if not mt5.initialize(login=1002947504, server="ClearInvestimentos-CLEAR", password="Joh0516"):
    print("initialize() Falha ao Iniciar seu metra Trade 5")
    mt5.shutdown()

    
def get_ohlc(ativo, timeframe, n=5):
    ativo = mt5.copy_rates_from_pos(ativo,timeframe, 0, n)
    ativo = pd.DataFrame(ativo)
    ativo['time'] = pd.to_datetime(ativo['time'], unit='s')
    ativo['Pivot'] = (ativo['high'] + ativo['low'] + ativo['close'])/3
    ativo['R1'] = 2*ativo['Pivot'] - ativo['low']
    ativo['S1'] = 2*ativo['Pivot'] - ativo['high']
    ativo['R2'] = ativo['Pivot'] + (ativo['high'] - ativo['low'])
    ativo['S2'] = ativo['Pivot'] - (ativo['high'] - ativo['low'])
    ativo['R3'] = ativo['Pivot'] + 2*(ativo['high'] - ativo['low'])
    ativo['S3'] = ativo['Pivot'] - 2*(ativo['high'] - ativo['low'])

    
    ativo.set_index('time', inplace = True)
    return ativo

ativo = (get_ohlc(ticker, mt5.TIMEFRAME_M5))
#display(ativo)

#testando se o ativo é valido 
symbol = ticker
symbol_info = mt5.symbol_info(symbol)
if symbol_info is None:
    print(symbol, "Não encontrato")
    mt5.shutdown()
    quit()
    
#adicionado symbol se nao existir
if not symbol_info.visible:
    print('Symbol Não visivel, tentnado adicionar')
    if not mt5.symbol_select(symbol,True):
        print('symbol_select({{}})failed, exit', symbol)
        mt5.shutdown()
        quit()

#preparando a ordem compra request  e ordem de venda

#lot = 100.0
#lot = input('Quantos lotes? Exemplo: 1.0 ')
lot = 1.0
point = mt5.symbol_info(symbol).point
price = mt5.symbol_info_tick(symbol).ask
desviation = 1
request = {    
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_BUY,
    "price": price,
    "magic": 234000,
    "desviation": desviation,
    "comment": "prython script open",
    "type_time":mt5.ORDER_TIME_GTC,
    'type_filling':mt5.ORDER_FILLING_RETURN,
    
    }
#preparando a ordem de venda 
lot = 1.0
point = mt5.symbol_info(symbol).point
price=mt5.symbol_info_tick(symbol).bid
desviation = 1
request2={
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_SELL,
    "price": price,
    
    "deviation": desviation,
    "magic": 234000,
    "comment": "python script close",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_RETURN,
    }


tempo = time.time() + 18000
while time.time() < tempo:
    ativo = (get_ohlc(ticker, mt5.TIMEFRAME_M5))
    tick = mt5.symbol_info_tick(ticker)
    print (f'{ticker} - ultimo valor: {tick.last}, Topo do Book C: {tick.bid},Topo do Book V: {tick.ask}', tick.last>ativo['Pivot'][-1 -1], end  = '\r')
    if tick.last> ativo['Pivot'][-1 -1]:
        if mt5.positions_get(symbol=ticker) == () or mt5.positions_get(symbol=ticker)[0][5] == 1:
            #enviadno ordem de compra 
            result = mt5.order_send(request)
            print(f'1. Ordem COMPRA enviada:{lot} de {symbol} ao preço de {price} com desvio de {desviation}',end  = '\r')

    if tick.last <ativo['S1'][-1 -1]:
        
        if mt5.positions_get(symbol=ticker) == () or mt5.positions_get(symbol=ticker)[0][5] == 0:
            #enviadno ordem de venda 
            result = mt5.order_send(request2)
        #verificando a resultado da execulção 
            print(f'1. Ordem VENDA enviada: {lot} de {symbol} ao preço de {price} com desvio de {desviation}',end  = '\r')
        
    time.sleep(0.5)