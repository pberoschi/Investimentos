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

diaHoje = 4
diaAmanha = diaHoje + 1
diaHoje = str(diaHoje)

def run():
    
    symbol = "WING22"
    
    # CRIAÇÃO DOS CÁLCULOS (MÉDIAS)
    timezone = pytz.timezone("Etc/UTC")
    utc_from = datetime(2022, 2, diaAmanha, tzinfo=timezone)
    ratesM1 = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M1, utc_from, 600)
    ratesH1 = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_H1, utc_from, 10)
    rates_frameM1 = pd.DataFrame(ratesM1)
    rates_frameH1 = pd.DataFrame(ratesH1)
    rates_frameM1['time']=pd.to_datetime(rates_frameM1['time'], unit='s')
    rates_frameH1['time']=pd.to_datetime(rates_frameH1['time'], unit='s')
    dfM1 = rates_frameM1[['time','open','high','low','close']]
    dfH1 = rates_frameH1[['time','open','high','low','close']]

    #dfM1 = dfM1.loc[dfM1["time"].between('2022-1-4 10:01:00', '2022-1-4 18:00:00')]
    #dfH1 = dfH1.loc[dfH1["time"].between('2022-1-4 09:00:00', '2022-1-4 09:05:00')]
    dfM1 = dfM1.loc[dfM1["time"].between(f'2022-1-{diaHoje} 10:01:00', f'2022-1-{diaHoje} 18:20:00')] # ESTUDOS
    dfH1 = dfH1.loc[dfH1["time"].between(f'2022-1-{diaHoje} 08:05:00', f'2022-1-{diaHoje} 09:05:00')] # ESTUDOS

    #display(dfM1.head())
    #display(dfH1.head(1))
    print(dfM1.tail()) # ESTUDOS
    print('')
    print(dfH1.head()) # ESTUDOS


    openH1 = dfH1['open']
    highH1 = dfH1['high']
    lowH1 = dfH1['low']
    closeH1 = dfH1['close']

    openM1 = dfM1['open'].iloc[-1]
    highM1 = dfM1['open'].iloc[-1]
    lowM1 = dfM1['open'].iloc[-1]
    closeM1 = dfM1['open'].iloc[-1]
    print(closeM1)


    #PRIMEIRA VELA
    closeVela1 = closeH1 = dfH1['close'].iloc[-1]
    openVela1 = openH1 = dfH1['open'].iloc[-1]
    highVela1 = dfH1['high'].iloc[-1]
    lowVela1 = dfH1['low'].iloc[-1]
    pontos1 = highVela1 - lowVela1

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
            if closeVela2 >= highVela1 + 3.0:
                print('COMPRA')
                precoCompra = closeVela2
                precoGainCompra = precoCompra + pontos1
                precoLossCompra = lowVela1

                print(f'Compra: {precoCompra}')
                print(f'Gain: {precoGainCompra}')
                print(f'Loss: {precoLossCompra}') 
                print(f'Pontos: {pontos1}')

                # ENVIANDO ORDEM COMPRA 
                symbol = symbol
                lot = 1.0
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
                bot.sendMessage(-351556985, f'ESTRATÉGIA ROMPIMENTO: COMPRA PARA >> {symbol} <<') 

                print('ENCERRANDO OPERAÇÕES POR HOJE')
                time.sleep(36000)

        # VENDA
        elif closeVela1 > closeVela2:
            if closeVela2 <= lowVela1 - 3.0:
                parar = True
                print('VENDA')
                precoVenda = closeVela2
                precoGainVenda = precoVenda - pontos1
                precoLossVenda = highVela1

                print(f'Compra: {precoVenda}')
                print(f'Gain: {precoGainVenda}')
                print(f'Loss: {precoLossVenda}') 
                print(f'Pontos: {pontos1}')

                # ENVIANDO ORDEM VENDA    
                symbol = symbol
                lot = 1.0
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
                bot.sendMessage(-351556985, f'ESTRATÉGIA ROMPIMENTO: VENDA PARA >> {symbol} <<')

                print('ENCERRANDO OPERAÇÕES POR HOJE')
                time.sleep(36000)

        else:
            print('AGUARDANDO PRÓXIMO SINAL')

        
        
y=0
while y < 2:
    symbol = "WING22"
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
    if ('10:00' < agoraRes < '17:30'):
        run()
        #print(f'FALTAM ${AindaFalta} PARA ATINGIR ALVO DO DIA \n')
        print('Script executado com sucesso.\n\n'.upper())
          
        # 5 MINUTOS DE INTERVALO
        time.sleep(60)
    else:
        print('AGUARDANDO ABERTURA DE MERCADO')
        time.sleep(60)