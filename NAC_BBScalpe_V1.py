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

#if not mt5.initialize(login=54679378, server="MetaQuotes-Demo", password="hz7ulfri"):
if not mt5.initialize(login=1092947504, server="ClearInvestimentos-CLEAR", password="Joh0516"):
    print("initialize() failed, error code =",mt5.last_error())
    quit()
    
def WING22():
    symbol = "WING22"

    # CRIAÇÃO DOS CÁLCULOS (MÉDIAS)
    timezone = pytz.timezone("Etc/UTC")
    utc_from = datetime(2021, 12, 22, tzinfo=timezone)
    rates = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M2, utc_from, 285)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
    df = rates_frame[['time','open','high','low','close']]

    # Calculando as bandas de bollinger
    periodo = 20
    desvios = 2

    df["desvio"] = df["close"].rolling(periodo).std()
    df["MM"] = df["close"].rolling(periodo).mean()
    df["Banda_Sup"] = df["MM"] + (df["desvio"]*desvios)
    df["Banda_Inf"] = df["MM"] - (df["desvio"]*desvios)

    df = df.dropna(axis = 0) 
    df = df.tail()
    print(df)

    if (df['close'].iloc[-3] > df['Banda_Sup'].iloc[-3]) & (df['close'].iloc[-2] < df['Banda_Sup'].iloc[-2]):
        print('VENDA')

        # VENDA: CALCULOS
        bandaSup = df['Banda_Sup'].iloc[-2]
        closeSell = df['close'].iloc[-2]
        amplitudeCandle = df['high'].iloc[-2] - df['low'].iloc[-2]

        precoVenda = closeSell - 10
        precoLoss = df['high'].iloc[-1] + 10
        precoGain = precoVenda - amplitudeCandle

        print(f'Banda Superior: {bandaSup}')
        print(f'Amplitude Candle: {amplitudeCandle}')
        print(f'Fechamento: {closeSell}')
        print(f'Preço Venda: {precoVenda}')
        print(f'Stop: {precoLoss}')
        print(f'Gain: {precoGain}')

        # ENVIANDO ORDEM VENDA    
        symbol = symbol
        lot = 1.0
        point = mt5.symbol_info(symbol).point
        price=mt5.symbol_info_tick(symbol).bid
        desviation = 1
        requestVENDA={
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_SELL,
            #"price": price,
            "price": precoVenda,
            "sl": precoLoss,
            "tp": precoGain,
            "deviation": desviation,
            "magic": 234000,
            "comment": "python script close",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
            }    
        resultVENDA = mt5.order_send(requestVENDA)
        resultVENDA
        print('\nORDEM DE VENDA ENVIADA COM SUCESSO')


    elif (df['close'].iloc[-3] < df['Banda_Inf'].iloc[-3]) & (df['close'].iloc[-2] > df['Banda_Inf'].iloc[-2]):
        print('COMPRA')

        # COMPRA: CALCULOS
        bandaInf = df['Banda_Inf'].iloc[-2]
        closeBuy = df['close'].iloc[-2]
        amplitudeCandle = df['high'].iloc[-2] - df['low'].iloc[-2]

        precoCompra = closeBuy + 10
        precoLoss = df['low'].iloc[-1] - 10
        precoGain = precoCompra + amplitudeCandle

        print(f'Banda Inferior: {bandaInf}')
        print(f'Fechamento: {closeBuy}')
        print(f'Amplitude Candle: {amplitudeCandle}')
        print(f'Preço Compra: {precoCompra}')
        print(f'Stop: {precoLoss}')
        print(f'Gain: {precoGain} ')


        # ENVIANDO ORDEM COMPRA 
        symbol = symbol
        lot = 1.0
        point = mt5.symbol_info(symbol).point
        price = mt5.symbol_info_tick(symbol).ask
        desviation = 1
        requestCOMPRA = {    
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY,
            #"price": price,
            "price": precoCompra,
            "sl": precoLoss,
            "tp": precoGain,
            "magic": 234000,
            "desviation": desviation,
            "comment": "prython script open",
            "type_time":mt5.ORDER_TIME_GTC,
            'type_filling':mt5.ORDER_FILLING_IOC,
            }
        resultCOMPRA = mt5.order_send(requestCOMPRA)
        resultCOMPRA
        print('\nORDEM DE COMPRA ENVIADA COM SUCESSO')

    else:
        print('\nAGUARDANDO PRÓXIMO SINAL DE OPERAÇÃO')

y=0
while y < 2:
    symbol = "WING22"
    agora = datetime.now()
    print(f'Buscando dados...{agora}')
      
    AlvoDia = -3940.00 + 500.00
    balancoDia = mt5.account_info().balance
    AindaFalta = AlvoDia - balancoDia
    
    # HORARIO DAS OPERAÇÕES
    agora = datetime.now()
    agora1 = str(agora)
    agoraRes = agora1[11:16]
       
    
    if (balancoDia <= AlvoDia) & ('09:00' < agoraRes < '17:00'):
        WING22()
        
        # 2 MINUTOS DE INTERVALO
        time.sleep(120)
        
    else:
        print('OPERAÇÕES ENCERRADAS POR HOJE')
        time.sleep(120)