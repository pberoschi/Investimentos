from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import pandas as pd 
import time
import telepot
pd.options.mode.chained_assignment = None  # default='warn'

client = Client('jogobafi@gmail.com', 'Johnny321@')

def run():
    #Selecionando ATIVOS com base em critério de volume
    tickers = client.get_ticker()
    tabela = pd.DataFrame(tickers)

    #Listar em ordem DECRESCENTE
    #tabela = tabela.sort_values(by=['lastPrice'], ascending=False)
    tabela = tabela.sort_values(by=['volume'], ascending=False)

    #Extrair apenas o nome do Ativo
    ativosList = list(tabela['symbol'])

    #Criando uma lista com 20 ativos
    ativos = []
    for ativo in ativosList:
        if ativo[-1] == 'T':
            ativos.append(ativo)        
            ativos = ativos[:50]

    for ativo in ativos:
        print(ativo)
        resumo4 = client.get_klines(symbol = ativo, interval = client.KLINE_INTERVAL_15MINUTE)
        resumo5 = pd.DataFrame(resumo4, columns=['date','open','high','low','close','volume','close_time','asset_volume','n of trades','asset_column','taker_buy','based_asset_volume'])
        resumo6 = resumo5[['date','open','high','low','close','volume','n of trades']]
        resumo6.set_index('date', inplace=True)
        resumo6.index = pd.to_datetime(resumo6.index, unit='ms')
        #print(ativo)
        #display(resumo6.tail(2))
        #print(len(resumo6))
        
        # MACD
        resumo6['EMA12'] = resumo6.close.ewm(span=12).mean()
        resumo6['EMA26'] = resumo6.close.ewm(span=26).mean()
        resumo6['MACD'] = resumo6.EMA12 - resumo6.EMA26
        resumo6['signal'] = resumo6.MACD.ewm(span=9, adjust=False, min_periods=9).mean()
        resumo6['histog'] = resumo6['MACD'] - resumo6['signal']

        # SETUP 13.3
        OitentaMME = resumo6['close'].ewm(span=80).mean()
        TrezeMME = resumo6['close'].ewm(span=13).mean() 
        TresMME = resumo6['close'].ewm(span=3).mean()

        resumo6.insert(loc=6,column='MME 80',value=OitentaMME)
        resumo6.insert(loc=7,column='MME 13',value=TrezeMME)
        resumo6.insert(loc=8,column='MME 3',value=TresMME)

        # MONITORAMENTO    
        resumo6['flag'] = ''
        resumo6['sinal'] = ''

        #for i in range (100, len(resumo)): # ESTUDOS
        for i in range (1, len(resumo6)): # TRADE
            if (resumo6['MME 13'][i] < resumo6['MME 3'][i]) & (resumo6['MME 13'][i] > resumo6['MME 80'][i]) & (resumo6['histog'][i] >= 0):
                resumo6['flag'][i] = 'COMPRA'

            elif (resumo6['MME 13'][i] > resumo6['MME 3'][i]) & (resumo6['MME 13'][i] < resumo6['MME 80'][i]) & (resumo6['histog'][i] <= 0):
                resumo6['flag'][i] = 'VENDA'

        for x in range(1,len(resumo6)):
            if resumo6['flag'][x] == resumo6['flag'][x-1]:
                resumo6['sinal'][x] = ''
            else:
                resumo6['sinal'][x] = 'sinal'

          # MENSAGEM NA MUDANÇA DE CONDICAO
            if (resumo6['sinal'].iloc[-1] == 'sinal') & (resumo6['flag'].iloc[-3] == 'COMPRA'):
                bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
                bot.sendMessage(-351556985, f'COMPRA: {ativo}')

            elif (resumo6['sinal'].iloc[-1] == 'sinal') & (resumo6['flag'].iloc[-3] == 'VENDA'):
                bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
                bot.sendMessage(-351556985, f'VENDA: {ativo}')

        resumo6 = resumo6[['close','volume','MME 80','MME 3','MACD','histog','flag','sinal']]
        print(resumo6.tail(2))

    print('>>> FIM DA EXECUÇÃO! <<<')
        
while True:
    run()
    time.sleep(900)