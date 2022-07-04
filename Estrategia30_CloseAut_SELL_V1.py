# Estrategia30_CloseAut

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

#if not mt5.initialize(login=1092947504, server="ClearInvestimentos-DEMO", password="Joh0516"):
#if not mt5.initialize(login=1002947504, server="ClearInvestimentos-CLEAR", password="Joh0516"):
if not mt5.initialize(login=4999473749, server="MetaQuotes-Demo", password="elf4lnbx"):
#if not mt5.initialize(login=54679378, server="MetaQuotes-Demo", password="hz7ulfri"):
    print("initialize() failed, error code =",mt5.last_error())
    quit()
    
def GBPUSD():
    # CRIAÇÃO DAS ORDENS ABERTURA E FECHAMENTO
    # DOLAR ()
    #symbol = "EURUSD"
    #symbol = "WDOF22"
    symbol = "GBPUSD"
    #symbol = "USDJPY"
    item = symbol
    ativo = symbol

    print(symbol)

    def compra():
        symbol = ativo
        lot = 1.0
        point = mt5.symbol_info(symbol).point
        price = mt5.symbol_info_tick(symbol).ask
        desviation = 1
        requestCOMPRA = {    
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "sl": price - 50 * point,
            "tp": price + 50 * point,
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
            "sl": price + 50 * point,
            "tp": price - 50 * point,
            "deviation": desviation,
            "magic": 234000,
            "comment": "python script close",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
            }    
        resultVENDA = mt5.order_send(requestVENDA)
        resultVENDA

    def close_compra():
        info_posicoes = mt5.positions_get(symbol = "GBPUSD")
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
        info_posicoes = mt5.positions_get(symbol = "GBPUSD")
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
        #point = mt5.symbol_info(symbol).point
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
    timezone = pytz.timezone("Etc/UTC")
    utc_from = datetime(2021, 12, 22, tzinfo=timezone)
    rates = mt5.copy_rates_from(item, mt5.TIMEFRAME_M5, utc_from, 113)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
    resumo = rates_frame[['time','open','close','spread']]
    #resumo

    # SETUP 30.3
    TrintaMME = resumo['close'].ewm(span=30).mean() 
    TresMME = resumo['open'].ewm(span=3).mean()

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
    info_posicoes = mt5.positions_get(symbol = "GBPUSD")
    if info_posicoes:
        #print(info_posicoes)
        df = pd.DataFrame(list(info_posicoes), columns=info_posicoes[0]._asdict().keys())
        #display(df)
        ticket = df['ticket'].iloc[0]
        natureza = df['type'].iloc[0]

    flag = resumo['flag'].iloc[-1]

    # FORCE
    #resumo['sinal'].iloc[-1] = 'sinal'
    #resumo['flag'].iloc[-1] = 'COMPRA'


    # LÓGICA DE EXECUCAO

    # MENSAGEM NA MUDANÇA DE CONDICAO
    #if resumo['sinal'].iloc[-1] == 'sinal':
        #bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
        #bot.sendMessage(-351556985, f'ATENÇÃO! MUDANÇA DE STATUS: >> {item} - {flag} <<')
        #print('Dados encontrados e enviados via Telegram'.upper())

    # EXECUÇÃO EM CADA VARREDURA
    if resumo['flag'].iloc[-1] == 'COMPRA':
        if info_posicoes:
            if df['type'].iloc[0] == 1: # VENDA
                print('Posição Atual: VENDA')
                time.sleep(3)
                print('Fechando VENDA')
                close_venda()
                time.sleep(3)
                #print('Abrindo uma COMPRA')
                #compra()
                #time.sleep(3)
                #print('Venda Fechada, COMPRA ABERTA')
                #time.sleep(3)
            else:
                close_compra()
                print('AGUARDANDO PRÓXIMA LTB')
        else:
            #compra()
            time.sleep(3)
            print('AGUARDANDO PRÓXIMA LTB')

    else:
        if info_posicoes: # VENDA
            if df['type'].iloc[0] == 0: #COMPRA
                print('Posição Atual: COMPRA')
                time.sleep(1)
                print('Fechando COMPRA')
                close_compra()
                time.sleep(3)
                venda()
                print('Compra Fechada, VENDA ABERTA')
                time.sleep(3)
            else:
                print('VENDA EM ANDAMENTO')
        else:
            venda()
            time.sleep(3)
            print('VENDA ABERTA')

    # SCALPING AUTOMÁTICO NO MACD   
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
        if info_posicoes:
            bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
            bot.sendMessage(-351556985, f'ATENÇÃO! LUCRO MÁXIMO NA COMPRA: >> {item} <<')
            #print('Dados encontrados e enviados via Telegram'.upper())
            close_compra()
            print('ATENÇÃO! LUCRO MÁXIMO NA COMPRA. SCALPING REALIZADO')
            time.sleep(3)
            print('ENTRANDO EM NOVA COMPRA')
            time.sleep(3)
            compra()
            print('Mantendo a posição em COMPRA'.upper())
        else:
            print('Erro. Reveja as posições'.upper())

    if lucroVENDA == True:
        if info_posicoes:
            bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
            bot.sendMessage(-351556985, f'ATENÇÃO! LUCRO MÁXIMO NA VENDA: >> {item} <<')
            #print('Dados encontrados e enviados via Telegram'.upper())
            close_venda()
            print('ATENÇÃO! LUCRO MÁXIMO NA VENDA. SCALPING REALIZADO')
            time.sleep(3)
            print('ENTRANDO EM NOVA VENDA')
            time.sleep(3)
            #venda()
            print('Mantendo a posição em VENDA'.upper())
        else:
            print('Erro. Reveja as posições'.upper())

     # SCALPING MANUAL
    if info_posicoes:
        if df['profit'].iloc[0] >= 50.00:
            profitLUC = df['profit'].iloc[0]
            if df['type'].iloc[0] == 0:
                #close_compra()
                time.sleep(5)
                #compra()   
            else:
                #close_venda()
                time.sleep(5)
                #compra()

            print(f'LUCRO OBTIDO E EFETIVADO DE: ${profitLUC}')
            # ENVIO DE MSG COM O LUCRO OBTIDO:
            #bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
            #bot.sendMessage(-351556985, f'ATENÇÃO! LUCRO OBTIDO EM {item}: R$ {profitLUC}')

        if df['profit'].iloc[0] <= -180.00:
            profitPER = df['profit'].iloc[0]
            if df['type'].iloc[0] == 0:
                #close_compra()
                time.sleep(5)
                #compra() 
            else:
                #close_venda()
                time.sleep(5)
                #compra()

            print(f'PREJUÍZO FECHADO DE: ${profitPER}')
            # ENVIO DE MSG COM O PREJUÍZO OBTIDO:
            #bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
            #bot.sendMessage(-351556985, f'ATENÇÃO! PREJUÍZO OBTIDO EM {item}: R$ {profitPER}')

    print(resumo.tail(5))
    print('')
    print(f'FALTAM ${AindaFalta} PARA ATINGIR ALVO DO DIA \n')
    print('Script executado com sucesso.\n\n'.upper())
           
y=0
while y < 2:
    symbol = "GBPUSD"
    agora = datetime.now()
    print(f'Buscando dados...{agora}')
      
    AlvoDia = 100064.00 + 500.00
    balancoDia = mt5.account_info().balance
    AindaFalta = AlvoDia - balancoDia
    
    # HORARIO DAS OPERAÇÕES
    agora = datetime.now()
    agora1 = str(agora)
    agoraRes = agora1[11:16]
       
    
    if (balancoDia <= AlvoDia) & ('04:00' < agoraRes < '18:00'):
        GBPUSD()
        
        # ENVIO DE MSG DE INÍCIO DAS OPERAÇÕES:
        bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
        bot.sendMessage(-351556985, f'INÍCIO DAS OPERAÇÕES DE HOJE PARA O **{symbol}**')
        
        # 5 MINUTOS DE INTERVALO
        time.sleep(300)
        
    else:
        def encerramento():        
            # FECHANDO TODAS AS POSIÇÕES
            symbol = "GBPUSD"
            item = symbol
            ativo = symbol

            info_posicoes = mt5.positions_get(symbol = "GBPUSD")
            if info_posicoes:
                df = pd.DataFrame(list(info_posicoes), columns=info_posicoes[0]._asdict().keys())
                ticket = df['ticket'].iloc[0]
                natureza = df['type'].iloc[0]

            def close_compra():
                info_posicoes = mt5.positions_get(symbol = "GBPUSD")
                if info_posicoes:
                    df = pd.DataFrame(list(info_posicoes), columns=info_posicoes[0]._asdict().keys())
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
                info_posicoes = mt5.positions_get(symbol = "GBPUSD")
                if info_posicoes:
                    df = pd.DataFrame(list(info_posicoes), columns=info_posicoes[0]._asdict().keys())
                    ticket = df['ticket'].iloc[0]
                    natureza = df['type'].iloc[0]

                # FECHAMENTO de uma VENDA
                symbol = ativo
                ticket = int(ticket)
                position_id=ticket
                lot = 1.0
                #point = mt5.symbol_info(symbol).point
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

            print('>>> ENCERRANDO OPERAÇÕES POR HOJE <<<')
            time.sleep(2)
            if info_posicoes:
                if df['type'].iloc[0] == 0: # COMPRA
                    print('ENCONTRADA UMA COMPRA EM ANDAMENTO. FECHANDO')
                    close_compra()
                    time.sleep(3)
                    print('COMPRA FECHADA COM SUCESSO')
                    print(f'TODAS AS OPERAÇÕES DE HOJE FORAM ENCERRADAS COM SUCESSO - HORA ATUAL: {agora}')
                else:
                    print('ENCONTRADA UMA VENDA EM ANDAMENTO. FECHANDO')
                    close_venda()
                    time.sleep(3)
                    print('VENDA FECHADA COM SUCESSO')
                    print(f'TODAS AS OPERAÇÕES DE HOJE FORAM ENCERRADAS COM SUCESSO - HORA ATUAL: {agora}')
            else:
                print(f'TODAS AS OPERAÇÕES DE HOJE FORAM ENCERRADAS COM SUCESSO - HORA ATUAL: {agora}')
                
        x=0
        while x < 4:
            encerramento()
            time.sleep(15)
            print('\n *** GARANTINDO QUE TODAS AS OPERAÇÕES FORAM ENCERRADAS...POR FAVOR, AGUARDE! ***')
            x=x+1

        print(f'TUDO FINALIZADO. ATÉ AMANHÃ!')
        # ENVIO DE MSG:
        bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
        bot.sendMessage(-351556985, f'TODAS AS OPERAÇÕES DE HOJE PARA O ** {symbol} ** FORAM ENCERRADAS! ATÉ MAIS!')
        break