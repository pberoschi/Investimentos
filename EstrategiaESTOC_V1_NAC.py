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

     
symbol = "WING22"
item = symbol
ativo = symbol 

def run():
    print(symbol)
    
    # CRIAÇÃO DOS CÁLCULOS (MÉDIAS)
    #timezone = pytz.timezone("Etc/UTC")
    #utc_from = datetime(2021, 12, 24, tzinfo=timezone)
    #rates = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M5, utc_from, 289)
    #rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 123) # PARA 9 HORAS DE MERCADO, 108 BARRAS
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 210) # PARA 9 HORAS DE MERCADO, 108 BARRAS
    rates_frame = pd.DataFrame(rates)
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
    resumo = rates_frame[['time','open','high','low','close','tick_volume']]
    #resumo.tail()  
    
    
    # CALCULO DO ESTOCASTICO e MME 3
    n = 8
    highMax = resumo['high'].rolling(n).max() 
    lowMin = resumo['low'].rolling(n).min()

    #estocastico
    resumo['estoc %K'] = ((resumo['close'] - lowMin) / (highMax - lowMin)) * 100
    resumo['estoc %D'] = resumo['estoc %K'].rolling(3).mean()

    # estocastico lento
    resumo["EstocS %K"] = resumo["estoc %D"]
    resumo["EstocS %D"] = resumo["EstocS %K"].rolling(3).mean()
    #resumo2.dropna(inplace=True) #remover espaços em branco

     
    resumo['flag'] = ''
    resumo['sinal'] = ''

    for i in range (1, len(resumo)): # TRADE

        if resumo['EstocS %K'][i] > resumo['EstocS %D'][i]:
            resumo['flag'][i] = 'COMPRA'
        else:
            resumo['flag'][i] = 'VENDA'
        
    for x in range(1,len(resumo)):
        if resumo['flag'][x] == resumo['flag'][x-1]:
            resumo['sinal'][x] = ''
        else:
            resumo['sinal'][x] = 'sinal'
    
    
    # RESUMINDO A TABELA
    resumo = resumo[['time','open','high','low','close','EstocS %K','EstocS %D','flag','sinal']]
    
    # LÓGICA DE EXECUCAO
    # MENSAGEM NA MUDANÇA DE CONDICAO
    
    # FORCE PARA TESTES
    #resumo['sinal'].iloc[-1] = 'sinal'
    
    if resumo['sinal'].iloc[-1] == 'sinal':
        flag = resumo['flag'].iloc[-1]
        #bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
        #bot.sendMessage(-351556985, f' >> Estratégia ESTOC: {item} ({flag}) <<')
        print('Dados encontrados e enviados via Telegram'.upper())
    
    
    # RELATÓRIO DAS POSIÇÕES
    info_posicoes = mt5.positions_get(symbol = symbol)
    if info_posicoes:
        #print(info_posicoes)
        df = pd.DataFrame(list(info_posicoes), columns=info_posicoes[0]._asdict().keys())
        #display(df)
        ticket = df['ticket'].iloc[0]
        natureza = df['type'].iloc[0]

    # EXECUÇÃO EM CADA VARREDURA
    #if (resumo['flag'].iloc[-2] == 'COMPRA') & (resumo['sinal'].iloc[-2] == 'sinal') & (resumo['EstocS %K'].iloc[-2] >= resumo['EstocS %D'].iloc[-2]) & (resumo['EstocS %K'].iloc[-2] >= 0.00) & (resumo['EstocS %K'].iloc[-2] <= 30.00):
    if (resumo['flag'].iloc[-1] == 'COMPRA') & (resumo['sinal'].iloc[-1] == 'sinal') & (resumo['EstocS %K'].iloc[-1] >= resumo['EstocS %D'].iloc[-1]) & (resumo['EstocS %K'].iloc[-1] >= 0.00) & (resumo['EstocS %K'].iloc[-1] <= 30.00):
        
        def compra():
            # COMPRA: CALCULOS
            highBuy = resumo['high'].iloc[-2]
            lowBuy = resumo['low'].iloc[-2]
            amplitudeCandle = highBuy - lowBuy

            #precoCompra = closeBuy + 1
            precoCompra = highBuy + 1
            precoLoss = lowBuy - 1
            precoGain = precoCompra + amplitudeCandle

            print(f'Amplitude Candle: {amplitudeCandle}')
            print(f'Máxima: {highBuy}')
            print(f'Mínima: {lowBuy}')
            print(f'Preço Compra: {precoCompra}')
            print(f'Stop: {precoLoss}')
            print(f'Gain: {precoGain} ')

            symbol = "WING22"
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


        # ENVIANDO ORDEM DE COMPRA COM GAIN E LOSS SETADOS
        if info_posicoes:
            if df['type'].iloc[0] == 1: # VENDA
                print('Posição Atual: VENDA')
                time.sleep(3)
                print('Fechando VENDA')
                #close_venda()
                time.sleep(3)
                print('Abrindo uma COMPRA')
                compra()
                time.sleep(3)
                print('Venda Fechada, COMPRA ABERTA')
                bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
                bot.sendMessage(-351556985, f'Venda Fechada, COMPRA ABERTA: >> {item} <<')
                time.sleep(3)
            else:
                print('COMPRA EM ANDAMENTO')
        else:
            compra()
            time.sleep(3)
            print('COMPRA ABERTA')
            bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
            bot.sendMessage(-351556985, f'COMPRA ABERTA: >> {item} <<')



    #elif (resumo['flag'].iloc[-2] == 'VENDA') & (resumo['sinal'].iloc[-2] == 'sinal') & (resumo['EstocS %K'].iloc[-2] <= resumo['EstocS %D'].iloc[-2]) & (resumo['EstocS %K'].iloc[-2] <= 100.00) & (resumo['EstocS %K'].iloc[-2] >= 70.00):
    elif (resumo['flag'].iloc[-1] == 'VENDA') & (resumo['sinal'].iloc[-1] == 'sinal') & (resumo['EstocS %K'].iloc[-1] <= resumo['EstocS %D'].iloc[-1]) & (resumo['EstocS %K'].iloc[-1] <= 100.00) & (resumo['EstocS %K'].iloc[-1] >= 70.00):
           
        def venda():
            # VENDA: CALCULOS
            highSell = resumo['high'].iloc[-2]
            lowSell = resumo['low'].iloc[-2]
            amplitudeCandle = highSell - lowSell

            #precoVenda = closeSell - 1
            precoVenda = lowSell - 1
            precoLoss = highSell + 1
            precoGain = precoVenda - amplitudeCandle

            print(f'Amplitude Candle: {amplitudeCandle}')
            print(f'Máxima: {highSell}')
            print(f'Mínima: {lowSell}')
            print(f'Preço Venda: {precoVenda}')
            print(f'Stop: {precoLoss}')
            print(f'Gain: {precoGain}')
  
            symbol = "WING22"
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
        
        # ENVIANDO ORDEM DE VENDA COM GAIN E LOSS SETADOS
        if info_posicoes: # VENDA
            if df['type'].iloc[0] == 0: #COMPRA
                print('Posição Atual: COMPRA')
                time.sleep(1)
                print('Fechando COMPRA')
                #close_compra()
                time.sleep(3)
                venda()
                print('Compra Fechada, VENDA ABERTA')
                bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
                bot.sendMessage(-351556985, f'Compra Fechada, VENDA ABERTA: >> {item} <<')
                time.sleep(3)
            else:
                print('VENDA EM ANDAMENTO')
        else:
            venda()
            time.sleep(3)
            print('VENDA ABERTA')
            bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
            bot.sendMessage(-351556985, f'VENDA ABERTA: >> {item} <<')
    

    print(resumo.tail())

      
'''          
y=0
while y < 2:
    symbol = symbol
    agora = datetime.now()
    print(f'Buscando dados...{agora}')
      
    AlvoDia = 99642.78 + 100.00
    balancoDia = mt5.account_info().balance
    AindaFalta = AlvoDia - balancoDia
    
    # HORARIO DAS OPERAÇÕES
    agora = datetime.now()
    agora1 = str(agora)
    agoraRes = agora1[11:16]
       
    
    #if (balancoDia <= AlvoDia) & ('04:00' < agoraRes < '18:00'):
    if balancoDia <= AlvoDia:
        run()
        print(f'FALTAM ${AindaFalta} PARA ATINGIR ALVO DO DIA \n')
        print('Script executado com sucesso.\n\n'.upper())
        
        # 5 MINUTOS DE INTERVALO
        time.sleep(300)
        
    else:
        def encerramento():        
            # FECHANDO TODAS AS POSIÇÕES
            symbol = "WDOF22"
            item = symbol
            ativo = symbol

            info_posicoes = mt5.positions_get(symbol = symbol)
            if info_posicoes:
                df = pd.DataFrame(list(info_posicoes), columns=info_posicoes[0]._asdict().keys())
                ticket = df['ticket'].iloc[0]
                natureza = df['type'].iloc[0]

            def close_compra():
                info_posicoes = mt5.positions_get(symbol = "WDOF22")
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
                info_posicoes = mt5.positions_get(symbol = "WDOF22")
                if info_posicoes:
                    df = pd.DataFrame(list(info_posicoes), columns=info_posicoes[0]._asdict().keys())
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
'''