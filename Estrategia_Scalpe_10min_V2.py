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

#diaHoje = 20
#diaAmanha = diaHoje + 1
#diaHoje = str(diaHoje)

def wdo():
    
    symbol = "WDOG22"
    print('')
    print(f'>> {symbol} <<')
    print('')
    
    ratesM1 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 910)   
    ratesM10 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M10, 0, 210)
    rates_frameM1 = pd.DataFrame(ratesM1)
    rates_frameM10 = pd.DataFrame(ratesM10)
    rates_frameM1['time']=pd.to_datetime(rates_frameM1['time'], unit='s')
    rates_frameM10['time']=pd.to_datetime(rates_frameM10['time'], unit='s')
    dfM1 = rates_frameM1[['time','open','high','low','close']]
    dfM10 = rates_frameM10[['time','open','high','low','close']]

    #dfM1 = dfM1.loc[dfM1["time"].between('2022-1-19 09:00:00', '2022-1-19 10:10:00')] # ESTUDOS
    #dfM10 = dfM10.loc[dfM10["time"].between('2022-1-18 09:00:00', '2022-1-18 09:21:00')] # ESTUDOS

    print('VELA 2')
    print(dfM1.tail()) # ESTUDOS
    print('')
    print('VELA 1')
    print(dfM10.tail()) # ESTUDOS

    closeM1 = dfM1['close'].iloc[-1]
    print(closeM1)

    #PRIMEIRA VELA
    closeVela1 = dfM10['close'].iloc[-2]
    openVela1 = dfM10['open'].iloc[-2]
    highVela1 = dfM10['high'].iloc[-2]
    lowVela1 = dfM10['low'].iloc[-2]
    pontos1 = (highVela1 - lowVela1) / 2
    #pontos1 = int(round(pontos1/5,0)*5)

    #SEGUNDA VELA
    closeVela2 = closeM1

    
    # RELATÓRIO DAS POSIÇÕES
    info_posicoes = mt5.positions_get(symbol = symbol)
    if info_posicoes:
        #print(info_posicoes)
        df = pd.DataFrame(list(info_posicoes), columns=info_posicoes[0]._asdict().keys())
        #display(df)
        ticket = df['ticket'].iloc[0]
        natureza = df['type'].iloc[0]
            
      
    #COMPRA 
    if info_posicoes:
        print('JÁ EXISTEM POSIÇÕES ABERTAS')
    else:
        if closeVela1 < closeVela2:
            if closeVela2 >= highVela1 + 1:
                price = mt5.symbol_info_tick(symbol).ask
                print('COMPRA')
                precoCompra = price
                precoGainCompra = precoCompra + pontos1
                precoLossCompra = lowVela1 - 2

                print(f'Compra: {precoCompra}')
                print(f'Gain: {precoGainCompra}')
                print(f'Loss: {precoLossCompra}') 
                print(f'Pontos: {pontos1}')

                # ENVIANDO ORDEM COMPRA 
                symbol = symbol
                lot = 3.0
                point = mt5.symbol_info(symbol).point
                #price = mt5.symbol_info_tick(symbol).ask
                #price = precoCompra
                desviation = 1

                requestCOMPRA = {    
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": symbol,
                    "volume": lot,
                    "type": mt5.ORDER_TYPE_BUY,
                    "price": precoCompra,
                    "sl": precoLossCompra,
                    "tp": precoGainCompra,
                    "magic": 234000,
                    "desviation": desviation,
                    "comment": "prython script open",
                    "type_time":mt5.ORDER_TIME_GTC,
                    'type_filling':mt5.ORDER_FILLING_IOC,
                    }
                resultCOMPRA = mt5.order_send(requestCOMPRA)
                resultCOMPRA
                print('\nORDEM DE COMPRA ENVIADA COM SUCESSO')
                
                bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
                bot.sendMessage(-351556985, f'ESTRATÉGIA ROMPIMENTO 10M: COMPRA PARA >> {symbol} <<') 

                print('ENCERRANDO OPERAÇÕES POR HOJE')
                time.sleep(1)

        # VENDA
        elif closeVela1 > closeVela2:
            if closeVela2 <= lowVela1 - 1:
                price=mt5.symbol_info_tick(symbol).bid
                parar = True
                print('VENDA')
                precoVenda = price
                precoGainVenda = precoVenda - pontos1
                precoLossVenda = highVela1 + 2

                print(f'Venda: {precoVenda}')
                print(f'Gain: {precoGainVenda}')
                print(f'Loss: {precoLossVenda}') 
                print(f'Pontos: {pontos1}')

                # ENVIANDO ORDEM VENDA    
                symbol = symbol
                lot = 2.0
                point = mt5.symbol_info(symbol).point
                #price=mt5.symbol_info_tick(symbol).bid
                #price=precoVenda
                desviation = 1

                requestVENDA={
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": symbol,
                    "volume": lot,
                    "type": mt5.ORDER_TYPE_SELL,
                    "price": precoVenda,
                    "sl": precoLossVenda,
                    "tp": precoGainVenda,
                    "deviation": desviation,
                    "magic": 234000,
                    "comment": "python script close",
                    "type_time": mt5.ORDER_TIME_GTC,
                    "type_filling": mt5.ORDER_FILLING_IOC,
                    }    
                resultVENDA = mt5.order_send(requestVENDA)
                resultVENDA
                print('\nORDEM DE VENDA ENVIADA COM SUCESSO')

                bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
                bot.sendMessage(-351556985, f'ESTRATÉGIA ROMPIMENTO 10M: VENDA PARA >> {symbol} <<')

                print('ENCERRANDO OPERAÇÕES POR HOJE')
                time.sleep(1)

        else:
            print('AGUARDANDO PRÓXIMO SINAL')

def win():
    
    symbol = "WING22"
    print('')
    print(f'>> {symbol} <<')
    print('')
    
    ratesM1 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 910)   
    ratesM10 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M10, 0, 210)
    rates_frameM1 = pd.DataFrame(ratesM1)
    rates_frameM10 = pd.DataFrame(ratesM10)
    rates_frameM1['time']=pd.to_datetime(rates_frameM1['time'], unit='s')
    rates_frameM10['time']=pd.to_datetime(rates_frameM10['time'], unit='s')
    dfM1 = rates_frameM1[['time','open','high','low','close']]
    dfM10 = rates_frameM10[['time','open','high','low','close']]

    #dfM1 = dfM1.loc[dfM1["time"].between('2022-1-19 09:00:00', '2022-1-19 10:10:00')] # ESTUDOS
    #dfM10 = dfM10.loc[dfM10["time"].between('2022-1-18 09:00:00', '2022-1-18 09:21:00')] # ESTUDOS

    print('VELA 2')
    print(dfM1.tail()) # ESTUDOS
    print('')
    print('VELA 1')
    print(dfM10.tail()) # ESTUDOS


    closeM1 = dfM1['close'].iloc[-1]
    print(f'Close Vela 2: {closeM1}')


    #PRIMEIRA VELA
    closeVela1 = dfM10['close'].iloc[-2]
    openVela1 = dfM10['open'].iloc[-2]
    highVela1 = dfM10['high'].iloc[-2]
    lowVela1 = dfM10['low'].iloc[-2]
    pontos1 = (highVela1 - lowVela1) / 2
    pontos1 = int(round(pontos1/5,0)*5)

    #SEGUNDA VELA
    closeVela2 = closeM1

    
    # RELATÓRIO DAS POSIÇÕES
    info_posicoes = mt5.positions_get(symbol = symbol)
    if info_posicoes:
        #print(info_posicoes)
        df = pd.DataFrame(list(info_posicoes), columns=info_posicoes[0]._asdict().keys())
        #display(df)
        ticket = df['ticket'].iloc[0]
        natureza = df['type'].iloc[0]
            
      
    #COMPRA 
    if info_posicoes:
        print('JÁ EXISTEM POSIÇÕES ABERTAS')
    else:
        if closeVela1 < closeVela2:
            if closeVela2 >= highVela1 + 30:
                price = mt5.symbol_info_tick(symbol).ask
                print('COMPRA')
                precoCompra = price
                precoGainCompra = precoCompra + pontos1
                precoLossCompra = lowVela1 - 30

                print(f'Compra: {precoCompra}')
                print(f'Gain: {precoGainCompra}')
                print(f'Loss: {precoLossCompra}') 
                print(f'Pontos: {pontos1}')

                # ENVIANDO ORDEM COMPRA 
                symbol = symbol
                lot = 3.0
                point = mt5.symbol_info(symbol).point
                #price = mt5.symbol_info_tick(symbol).ask
                #price = precoCompra
                desviation = 1

                requestCOMPRA = {    
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": symbol,
                    "volume": lot,
                    "type": mt5.ORDER_TYPE_BUY,
                    "price": precoCompra,
                    #"sl": precoLossCompra,
                    #"tp": precoGainCompra,
                    "magic": 234000,
                    "desviation": desviation,
                    "comment": "prython script open",
                    "type_time":mt5.ORDER_TIME_GTC,
                    'type_filling':mt5.ORDER_FILLING_IOC,
                    }
                resultCOMPRA = mt5.order_send(requestCOMPRA)
                resultCOMPRA
                print('\nORDEM DE COMPRA ENVIADA COM SUCESSO')
                
                bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
                bot.sendMessage(-351556985, f'ESTRATÉGIA ROMPIMENTO 10M: COMPRA PARA >> {symbol} <<') 

                print('ENCERRANDO OPERAÇÕES POR HOJE')
                time.sleep(1)

        # VENDA
        elif closeVela1 > closeVela2:
            if closeVela2 <= lowVela1 - 30:
                price=mt5.symbol_info_tick(symbol).bid
                parar = True
                print('VENDA')
                precoVenda = price
                precoGainVenda = precoVenda - pontos1
                precoLossVenda = highVela1 + 30

                print(f'Venda: {precoVenda}')
                print(f'Gain: {precoGainVenda}')
                print(f'Loss: {precoLossVenda}') 
                print(f'Pontos: {pontos1}')

                # ENVIANDO ORDEM VENDA    
                symbol = symbol
                lot = 3.0
                point = mt5.symbol_info(symbol).point
                #price=mt5.symbol_info_tick(symbol).bid
                #price=precoVenda
                desviation = 1

                requestVENDA={
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": symbol,
                    "volume": lot,
                    "type": mt5.ORDER_TYPE_SELL,
                    "price": precoVenda,
                    "sl": precoLossVenda,
                    "tp": precoGainVenda,
                    "deviation": desviation,
                    "magic": 234000,
                    "comment": "python script close",
                    "type_time": mt5.ORDER_TIME_GTC,
                    "type_filling": mt5.ORDER_FILLING_IOC,
                    }    
                resultVENDA = mt5.order_send(requestVENDA)
                resultVENDA
                print('\nORDEM DE VENDA ENVIADA COM SUCESSO')

                bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
                bot.sendMessage(-351556985, f'ESTRATÉGIA ROMPIMENTO 10M: VENDA PARA >> {symbol} <<')

                print('ENCERRANDO OPERAÇÕES POR HOJE')
                time.sleep(1)

        else:
            print('AGUARDANDO PRÓXIMO SINAL')
     
        
while True:
    symbol = "WDOG22"
    agora = datetime.now()
    print(f'Buscando dados...{agora}')
      
    AlvoDia = -3900.00 + 500.00
    balancoDia = mt5.account_info().balance
    AindaFalta = AlvoDia - balancoDia
    
    # HORARIO DAS OPERAÇÕES
    agora = datetime.now()
    agora1 = str(agora)
    agoraRes = agora1[11:16]
       
 
    #if (balancoDia <= AlvoDia) & ('09:00' < agoraRes < '17:30'):
    if ('09:10' < agoraRes < '09:20'):
        wdo()
        time.sleep(1)
        win()
        #print(f'FALTAM ${AindaFalta} PARA ATINGIR ALVO DO DIA \n')
        print('Script executado com sucesso.\n\n'.upper())
          
        #INTERVALO
        time.sleep(60)
    else:
        print('AGUARDANDO ABERTURA DE MERCADO')
        time.sleep(60)