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

#if not mt5.initialize(login=1002947504, server="ClearInvestimentos-CLEAR", password="Joh0516"):
if not mt5.initialize(login=1092947504, server="ClearInvestimentos-DEMO", password="Joh0516"):
#if not mt5.initialize(login=4999473749, server="MetaQuotes-Demo", password="elf4lnbx"):
    print("initialize() failed, error code =",mt5.last_error())
    quit()

symbol = "WDOG22"

def run():
    symbol = "WDOG22"
    #symbol = "WDOF22"
    item = symbol
    ativo = symbol 
    print(symbol)
    
    # CRIAÇÃO DAS ORDENS ABERTURA E FECHAMENTO
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
            "sl": price - 10000 * point,
            #"tp": price + 50 * point,
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
            "sl": price + 10000 * point,
            #"tp": price - 50 * point,
            "deviation": desviation,
            "magic": 234000,
            "comment": "python script close",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
            }    
        resultVENDA = mt5.order_send(requestVENDA)
        resultVENDA

    def close_compra():
        info_posicoes = mt5.positions_get(symbol = "WDOG22")
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
        info_posicoes = mt5.positions_get(symbol = "WDOG22")
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
    #timezone = pytz.timezone("Etc/UTC")
    #utc_from = datetime(2021, 12, 28, tzinfo=timezone)
    #rates = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M5, utc_from, 289)
    #rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 123) # PARA 9 HORAS DE MERCADO, 108 BARRAS
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M10, 0, 150) # PARA 9 HORAS DE MERCADO, 108 BARRAS
    rates_frame = pd.DataFrame(rates)
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
    resumo = rates_frame[['time','open','high','low','close','tick_volume']]
    #resumo.tail()  
   
    
    # SETUP 34.8
    TquadroMME = resumo['close'].ewm(span=34).mean() 
    OitoMME = resumo['close'].ewm(span=8).mean()

    resumo.insert(loc=4,column='MME 34',value=TquadroMME)
    resumo.insert(loc=5,column='MME 8',value=OitoMME)
    
    #display(resumo.tail(60))
    #resumo = resumo.loc[resumo["time"].between('2021-12-22 14:00:00', '2021-12-23 18:20:00')]
    #display(resumo.tail())
    
    
    # MACD
    resumo['EMA12'] = resumo.close.ewm(span=12).mean()
    resumo['EMA26'] = resumo.close.ewm(span=26).mean()
    resumo['MACD'] = resumo.EMA12 - resumo.EMA26
    #resumo['signal'] = resumo.MACD.ewm(span=9).mean()
    resumo['signal'] = resumo.MACD.ewm(span=9, adjust=False, min_periods=9).mean()
    resumo['histog'] = resumo['MACD'] - resumo['signal']
    #display(resumo.tail(60))
    #teste = resumo[['MACD','signal','histog']]
    #display(resumo.tail(10))
    
    
    # MONITORAMENTO    
    resumo['flag'] = ''
    resumo['sinal'] = ''

    #for i in range (100, len(resumo)): # ESTUDOS
    for i in range (1, len(resumo)): # TRADE

        if resumo['MME 34'][i] < resumo['MME 8'][i]:
            resumo['flag'][i] = 'COMPRA'
        else:
            resumo['flag'][i] = 'VENDA'
        
    for x in range(1,len(resumo)):
        if resumo['flag'][x] == resumo['flag'][x-1]:
            resumo['sinal'][x] = ''
        else:
            resumo['sinal'][x] = 'sinal'
    
    
    # RELATÓRIO DAS POSIÇÕES
    info_posicoes = mt5.positions_get(symbol = symbol)
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
    if resumo['sinal'].iloc[-1] == 'sinal':
        bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
        bot.sendMessage(-351556985, f'ATENÇÃO! MUDANÇA DE STATUS: >> {item} - {flag} <<')
        print('Dados encontrados e enviados via Telegram'.upper())

    # EXECUÇÃO EM CADA VARREDURA
    if (resumo['flag'].iloc[-1] == 'COMPRA') & (resumo['flag'].iloc[-3] == 'VENDA'):
        if info_posicoes:
            if df['type'].iloc[0] == 1: # VENDA
                print('Posição Atual: VENDA')
                time.sleep(3)
                print('Fechando VENDA')
                close_venda()
                time.sleep(3)
                print('Abrindo uma COMPRA')
                compra()
                time.sleep(3)
                print('Venda Fechada, COMPRA ABERTA')
                time.sleep(3)
            else:
                print('COMPRA EM ANDAMENTO')
        else:
            compra()
            time.sleep(3)
            print('COMPRA ABERTA')

    elif (resumo['flag'].iloc[-1] == 'VENDA') & (resumo['flag'].iloc[-3] == 'COMPRA'):
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
    else:
        print('AGUARDANDO PRÓXIMA CONDIÇÃO DE OPERAÇÃO')

    
    # SCALPING AUTOMÁTICO NO MACD   
    resumo['lucroVENDA'] = ''
    resumo['lucroCOMPRA'] = ''

    # VENDA
    if (resumo['signal'].iloc[-1] < 0) & (resumo['histog'].iloc[-1] > 0) & (resumo['flag'].iloc[-1] == 'VENDA'):
        resumo['lucroVENDA'].iloc[-1] = 'LUCRO V'
        if info_posicoes:
            resultadoV = df['profit'].iloc[-1]
            bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
            bot.sendMessage(-351556985, f'ATENÇÃO! LUCRO MÁXIMO NA VENDA: >> {item} ${resultadoV}<<')
            #print('Dados encontrados e enviados via Telegram'.upper())
            close_venda()
            print('ATENÇÃO! LUCRO MÁXIMO NA VENDA. SCALPING REALIZADO')
            time.sleep(3)
        #else:
            #print('Erro. Reveja as posições'.upper())
    else:
        resumo['lucroVENDA'].iloc[-1] = ''
        
    # COMPRA
    if (resumo['signal'].iloc[-1] > 0) & (resumo['histog'].iloc[-1] < 0) & (resumo['flag'].iloc[-1] == 'COMPRA'):
        resumo['lucroCOMPRA'].iloc[-1] = 'LUCRO C'
        if info_posicoes:
            resultadoC = df['profit'].iloc[-1]
            bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
            bot.sendMessage(-351556985, f'ATENÇÃO! LUCRO MÁXIMO NA COMPRA: >> {item} ${resultadoC}<<')
            #print('Dados encontrados e enviados via Telegram'.upper())
            close_compra()
            print('ATENÇÃO! LUCRO MÁXIMO NA COMPRA. SCALPING REALIZADO')
            time.sleep(3)
        #else:
            #print('Erro. Reveja as posições'.upper())

    else:
        resumo['lucroCOMPRA'].iloc[-1] = ''  

    print(resumo.tail(5))
    print('')


while True:
    run()
    time.sleep(600)




'''                 
y=0
while y < 2:
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
       
    
    
    if (balancoDia <= AlvoDia) & ('09:00' < agoraRes < '17:30'):
        run()
        print(f'FALTAM ${AindaFalta} PARA ATINGIR ALVO DO DIA \n')
        print('Script executado com sucesso.\n\n'.upper())
          
        # 5 MINUTOS DE INTERVALO
        time.sleep(300)
        
    else:
        def encerramento():        
            # FECHANDO TODAS AS POSIÇÕES
            symbol = "WDOG22"
            item = symbol
            ativo = symbol

            info_posicoes = mt5.positions_get(symbol = "WDOG22")
            df = pd.DataFrame(list(info_posicoes), columns=info_posicoes[0]._asdict().keys())
            ticket = df['ticket'].iloc[0]
            natureza = df['type'].iloc[0]

            def close_compra():
                info_posicoes = mt5.positions_get(symbol = "WDOG22")
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
                info_posicoes = mt5.positions_get(symbol = "WDOG22")
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
           info_posicoes = mt5.positions_get(symbol = "WDOG22")
           if info_posicoes:
              encerramento()
              time.sleep(15)
              print('\n *** GARANTINDO QUE TODAS AS OPERAÇÕES FORAM ENCERRADAS...POR FAVOR, AGUARDE! ***')
              x=x+1
           else:
              print('NÃO HÁ POSIÇÕES A SEREM FECHADAS!')
              time.sleep(1)
              x=x+1
         
        print(f'TUDO FINALIZADO. ATÉ AMANHÃ!')
        # ENVIO DE MSG:
        bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
        bot.sendMessage(-351556985, f'TODAS AS OPERAÇÕES DE HOJE PARA O ** {symbol} ** FORAM ENCERRADAS! ATÉ MAIS!')
        time.sleep(300)
        break
'''