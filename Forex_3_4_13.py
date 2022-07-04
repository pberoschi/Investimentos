#ESTRATÉGIA Rápida e Lenta
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager 
import pandas as pd 
import time 
import telepot 

pd.options.mode.chained_assignment = None # default='warn'

client = Client('jogobafi@gmail.com', 'Johnny321@')

def run():
    ativos = ['BTCUSDT','ETHUSDT','EOSUSDT','NEOUSDT']

    MME_Rapida = 3
    MME_Lenta = 4 #open
    
    for ativo in ativos:
        print(ativo) 
        resumo4 = client.get_klines(symbol = ativo, interval = client.KLINE_INTERVAL_30MINUTE) 
        resumo5 = pd.DataFrame(resumo4, columns=['date','open','high','low','close','volume','close_time','asset_volume','n of trades','asset_column','taker_buy','based_asset_volume']) 
        resumo6 = resumo5[['date','open','high','low','close','volume','n of trades']] 
        resumo6.set_index('date', inplace=True) 
        resumo6.index = pd.to_datetime(resumo6.index, unit='ms') 
        #print(ativo) 
        #display(resumo6.tail(2)) 
        #print(len(resumo6))

        #SETUP 3.4
        MMERapida = resumo6['close'].ewm(span=MME_Rapida).mean() 
        #MMELenta = resumo6['close'].ewm(span=MME_Lenta).mean()
        MMELenta = resumo6['open'].ewm(span=MME_Lenta).mean()

        resumo6.insert(loc=6,column='MME Rápida',value=MMERapida) 
        resumo6.insert(loc=7,column='MME Lenta',value=MMELenta)

        #MONITORAMENTO
        resumo6['flag'] = '' 
        resumo6['sinal'] = ''

        #for i in range (100, len(resumo)): 
        # ESTUDOS 

        for i in range (1, len(resumo6)): # TRADE 
            if (resumo6['MME Rápida'][i] > resumo6['MME Lenta'][i]): 
                resumo6['flag'][i] = 'COMPRA'

            elif (resumo6['MME Rápida'][i] < resumo6['MME Lenta'][i]):
                resumo6['flag'][i] = 'VENDA'

        for x in range(1,len(resumo6)): 
            if resumo6['flag'][x] == resumo6['flag'][x-1]:
                resumo6['sinal'][x] = '' 
            else: resumo6['sinal'][x] = 'sinal'

        #MENSAGEM NA MUDANÇA DE CONDICAO
        if (resumo6['sinal'].iloc[-2] == 'sinal') & (resumo6['flag'].iloc[-2] == 'COMPRA'):
            bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
            bot.sendMessage(-351556985, f'COMPRA: {ativo}')

        elif (resumo6['sinal'].iloc[-2] == 'sinal') & (resumo6['flag'].iloc[-2] == 'VENDA'):
            bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
            bot.sendMessage(-351556985, f'VENDA: {ativo}')

        resumo6 = resumo6[['open','close','volume','MME Rápida','MME Lenta','flag','sinal']] 
        print(resumo6.tail(2))

    print('>>> FIM DA EXECUÇÃO! <<<')

while True:
    run()
    #time.sleep(3600)
    time.sleep(1800)