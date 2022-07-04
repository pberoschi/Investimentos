# Copyright 2021, MetaQuotes Ltd.
# https://www.mql5.com

# RESERVA (1 ATIVO)
# COM MACD e SETUP 30.3

from datetime import datetime
import MetaTrader5 as mt5
import time
import telepot
import pytz

def eur():
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
    symbol = "EURUSD"
    item = symbol
    ativo = symbol

    print(symbol)


    def compra():
        symbol = ativo
        lot = 1.0
        #point = mt5.symbol_info(symbol).point
        price = mt5.symbol_info_tick(symbol).ask
        desviation = 1
        requestCOMPRA = {    
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "magic": 234000,
            "desviation": desviation,
            "comment": "prython script open",
            "type_time":mt5.ORDER_TIME_GTC,
            'type_filling':mt5.ORDER_FILLING_IOC,
            }
        resultCOMPRA = mt5.order_send(requestCOMPRA)
        resultCOMPRA

    def venda():
        symbol = ativo
        lot = 1.0
        point = mt5.symbol_info(symbol).point
        price=mt5.symbol_info_tick(symbol).bid
        desviation = 1
        requestVENDA={
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_SELL,
            "price": price,

            "deviation": desviation,
            "magic": 234000,
            "comment": "python script close",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
            }    
        resultVENDA = mt5.order_send(requestVENDA)
        resultVENDA

    def close_compra():
        info_posicoes = mt5.positions_get(symbol = "EURUSD")
        if info_posicoes:
            #print(info_posicoes)
            df = pd.DataFrame(list(info_posicoes), columns=info_posicoes[0]._asdict().keys())
            #display(df)
            ticket = df['ticket'].iloc[0]
            natureza = df['type'].iloc[0]

        # FECHAMENTO de uma COMPRA
        symbol = ativo
        ticket = int(ticket)
        position_id=ticket
        lot = 1.0
        #point = mt5.symbol_info(symbol).point
        price=mt5.symbol_info_tick(symbol).bid
        desviation = 1

        request2={
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_SELL,
            "position": position_id,
            "price": price,
            "deviation": desviation,
            "magic": 234000,
            "comment": "python script close",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
            }    
        result = mt5.order_send(request2)
        result

    def close_venda():
        info_posicoes = mt5.positions_get(symbol = "EURUSD")
        if info_posicoes:
            #print(info_posicoes)
            df = pd.DataFrame(list(info_posicoes), columns=info_posicoes[0]._asdict().keys())
            #display(df)
            ticket = df['ticket'].iloc[0]
            natureza = df['type'].iloc[0]

        # FECHAMENTO de uma VENDA
        symbol = ativo
        ticket = int(ticket)
        position_id=ticket
        lot = 1.0
        point = mt5.symbol_info(symbol).point
        price=mt5.symbol_info_tick(symbol).ask
        desviation = 1

        request2={
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY,
            "position": position_id,
            "price": price,
            "deviation": desviation,
            "magic": 234000,
            "comment": "python script close",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
            }    
        result = mt5.order_send(request2)
        result

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

    #flag = resumo['flag'].iloc[-1]


    # RELATÓRIO DAS POSIÇÕES
    info_posicoes = mt5.positions_get(symbol = "EURUSD")
    if info_posicoes:
        #print(info_posicoes)
        df = pd.DataFrame(list(info_posicoes), columns=info_posicoes[0]._asdict().keys())
        print(df)
        ticket = df['ticket'].iloc[-1]
        natureza = df['type'].iloc[-1]

    flag = resumo['flag'].iloc[-1]

    # FORCE
    #resumo['sinal'].iloc[-1] = 'sinal'
    #resumo['flag'].iloc[-1] = 'COMPRA'


    # LÓGICA DE EXECUCAO

    # MENSAGEM TELEGRAM PARA MUDANÇA DE CONDICAO
    #if resumo['sinal'].iloc[-1] == 'sinal':
        #bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
        #bot.sendMessage(-351556985, f'ATENÇÃO! MUDANÇA DE STATUS: >> {item} - {flag} <<')
        #print('Dados encontrados e enviados via Telegram'.upper())


    # EXECUÇÃO EM CADA VARREDURA
    if resumo['flag'].iloc[-1] == 'COMPRA':
        if info_posicoes:
            if df['type'].iloc[0] == 1: # VENDA
                print('Posição Atual: VENDA')
                time.sleep(1)
                print('Fechando VENDA')
                close_venda()
                time.sleep(1)
                if (resumo['close'].iloc[-2] >= resumo['close'].iloc[-3] >= resumo['close'].iloc[-4]) & (resumo['close'].iloc[-1] > resumo['signal'].iloc[-1]):
                    print('Abrindo uma COMPRA')
                    compra()
                    time.sleep(3)
            else:
                if (resumo['close'].iloc[-2] >= resumo['close'].iloc[-3] >= resumo['close'].iloc[-4]) & (resumo['close'].iloc[-1] > resumo['signal'].iloc[-1]):
                    print('COMPRA EM ANDAMENTO')
                else:
                    close_compra()
                    print('COMPRA FECHADA - MERCADO LATERAL')
        else:
            if (resumo['close'].iloc[-2] >= resumo['close'].iloc[-3] >= resumo['close'].iloc[-4]) & (resumo['close'].iloc[-1] > resumo['signal'].iloc[-1]):
                compra()
                print('COMPRA ABERTA - LTA')
            else:
                print('PAUSA - MERCADO LATERAL')
     
    
    else:
        if info_posicoes:
            if df['type'].iloc[0] == 0: #COMPRA
                print('Posição Atual: COMPRA')
                time.sleep(1)
                print('Fechando COMPRA')
                close_compra()
                time.sleep(1)
                if (resumo['close'].iloc[-2] <= resumo['close'].iloc[-3] <= resumo['close'].iloc[-4]) | (resumo['close'].iloc[-1] < resumo['signal'].iloc[-1]):
                    print('Abrindo uma VENDA')
                    venda()
                    time.sleep(3)
            else:
                if (resumo['close'].iloc[-2] <= resumo['close'].iloc[-3] <= resumo['close'].iloc[-4]) | (resumo['close'].iloc[-1] < resumo['signal'].iloc[-1]):
                    print('VENDA EM ANDAMENTO')
                else:
                    close_venda()
                    print('VENDA FECHADA - MERCADO LATERAL')
        else:
            if (resumo['close'].iloc[-2] <= resumo['close'].iloc[-3] <= resumo['close'].iloc[-4]) | (resumo['close'].iloc[-1] < resumo['signal'].iloc[-1]):
                venda()
                print('VENDA ABERTA - LTB')
            else:
                print('PAUSA - MERCADO LATERAL')

    time.sleep(5)


    # AVISO DE SAÍDA DA OPERAÇÃO    
    compraHISTOG = resumo['histog'].iloc[-4] > 0 and resumo['histog'].iloc[-3] > 0 and resumo['histog'].iloc[-2] > 0
    compraSIGNAL = resumo['signal'].iloc[-4] > 0 and resumo['signal'].iloc[-3] > 0 and resumo['signal'].iloc[-2] > 0    
    lucroCOMPRA = compraHISTOG and resumo['histog'].iloc[-1] < 0 and compraSIGNAL and resumo['signal'].iloc[-1] > 0
    resumo['lucroCOMPRA'] = lucroCOMPRA
    # FORCE
    #lucroCOMPRA = True

    vendaHISTOG = resumo['histog'].iloc[-4] < 0 and resumo['histog'].iloc[-3] < 0 and resumo['histog'].iloc[-2] < 0
    vendaSIGNAL = resumo['signal'].iloc[-4] < 0 and resumo['signal'].iloc[-3] < 0 and resumo['signal'].iloc[-2] < 0     
    lucroVENDA = compraHISTOG and resumo['histog'].iloc[-1] > 0 and compraSIGNAL and resumo['signal'].iloc[-1] < 0
    resumo['lucroVENDA'] = lucroVENDA
    # FORCE
    #lucroVENDA = True

    if lucroCOMPRA == True:
        bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
        bot.sendMessage(-351556985, f'ATENÇÃO! LUCRO MÁXIMO NA COMPRA: >> {item} <<')
        print('Dados encontrados e enviados via Telegram'.upper())
        close_compra()
        time.sleep(5)

    if lucroVENDA == True:
        bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
        bot.sendMessage(-351556985, f'ATENÇÃO! LUCRO MÁXIMO NA VENDA: >> {item} <<')
        print('Dados encontrados e enviados via Telegram'.upper())
        close_venda()
        time.sleep(5)
        
     # SCALPING AUTOMÁTICO
    #if info_posicoes:
        #if df['profit'].iloc[-1] >= 50.00:
            #profitLUC = df['profit'].iloc[0]
            #if df['type'].iloc[0] == 0:
                #close_compra()
                #time.sleep(5)
                #compra()   
                
            #else:
                #close_venda()
                #time.sleep(5)
                #compra()
                                
            #print(f'LUCRO OBTIDO E EFETIVADO DE: ${profitLUC}')
            # ENVIO DE MSG COM O LUCRO OBTIDO:
            #bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
            #bot.sendMessage(-351556985, f'ATENÇÃO! LUCRO OBTIDO EM {item}: R$ {profitLUC}')
                
        #if df['profit'].iloc[-1] <= -180.00:
            #profitPER = df['profit'].iloc[0]
            #if df['type'].iloc[0] == 0:
                #close_compra()
                #time.sleep(5)
                #compra() 
            #else:
                #close_venda()
                #time.sleep(5)
                #compra()
                
            #print(f'PREJUÍZO FECHADO DE: ${profitPER}')
            # ENVIO DE MSG COM O PREJUÍZO OBTIDO:
            #bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
            #bot.sendMessage(-351556985, f'ATENÇÃO! PREJUÍZO OBTIDO EM {item}: R$ {profitPER}')
        
    print(resumo.tail(5))
    time.sleep(2)

    print('')
    print('Script executado com sucesso. Fechando o programa...'.upper())
    #time.sleep()
    print('\n\n')


while True:
   eur()
   time.sleep(60)