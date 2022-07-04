# https://quantbrasil.com.br/como-identificar-linhas-de-suporte-e-resistencia-utilizando-python


from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import pandas as pd 
import time
import telepot
pd.options.mode.chained_assignment = None  # default='warn'

client = Client('jogobafi@gmail.com', 'Johnny321@')


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
    #print(ativo)
    #resumo4 = client.get_klines(symbol = ativo, interval = client.KLINE_INTERVAL_1HOUR)
    resumo4 = client.get_klines(symbol = ativo, interval = client.KLINE_INTERVAL_1DAY)
    resumo5 = pd.DataFrame(resumo4, columns=['date','open','high','low','close','volume','close_time','asset_volume','n of trades','asset_column','taker_buy','based_asset_volume'])
    resumo6 = resumo5[['date','open','high','low','close','volume','n of trades']]
    resumo6.set_index('date', inplace=True)
    resumo6.index = pd.to_datetime(resumo6.index, unit='ms')


    # IMPRESSÃO DOS VALORES #
    def Valores():
        LTA1 = resumo6['low'].iloc[-1]
        LTA2 = resumo6['low'].iloc[-2]
        LTA3 = resumo6['low'].iloc[-3]
        LTA4 = resumo6['low'].iloc[-4]
        LTA5 = resumo6['low'].iloc[-5]

        LTB1 = resumo6['high'].iloc[-1]
        LTB2 = resumo6['high'].iloc[-2]
        LTB3 = resumo6['high'].iloc[-3]
        LTB4 = resumo6['high'].iloc[-4]
        LTB5 = resumo6['high'].iloc[-5]


        print(f'(SUPORTE) LTA 5: {LTA5}')
        print(f'(SUPORTE) LTA 4: {LTA4}')
        print(f'(SUPORTE) LTA 3: {LTA3}')
        print(f'(SUPORTE) LTA 2: {LTA2}')
        print(f'(SUPORTE) LTA 1: {LTA1}')
        print('')
        print(f'(RESISTÊNCIA) LTB 5: {LTB5}')
        print(f'(RESISTÊNCIA) LTB 4: {LTB4}')
        print(f'(RESISTÊNCIA) LTB 3: {LTB3}')
        print(f'(RESISTÊNCIA) LTB 2: {LTB2}')
        print(f'(RESISTÊNCIA) LTB 1: {LTB1}')


    # MÉDIAS DE 200, 50 e 21
    resumo6['MA200'] = resumo6.close.ewm(span=200).mean()
    resumo6['MA50'] = resumo6.close.ewm(span=50).mean()
    resumo6['MA21'] = resumo6.close.ewm(span=21).mean()

    #if resumo6['low'].iloc[-2] > resumo6['low'].iloc[-3] > resumo6['low'].iloc[-4] < resumo6['low'].iloc[-5] < resumo6['low'].iloc[-6]:
    if (resumo6['low'].iloc[-2] > resumo6['low'].iloc[-3] > resumo6['low'].iloc[-4] < resumo6['low'].iloc[-5] < resumo6['low'].iloc[-6]) & (resumo6['MA21'].iloc[-2] > resumo6['MA50'].iloc[-2]) & (resumo6['MA50'].iloc[-2] > resumo6['MA200'].iloc[-2]):
        print(f'>>> {ativo}: COMPRA')
        bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
        bot.sendMessage(-351556985, f'COMPRA:..........{ativo}')
        #Valores()
        #print('')

    #elif resumo6['high'].iloc[-2] < resumo6['high'].iloc[-3] < resumo6['high'].iloc[-4] > resumo6['high'].iloc[-5] > resumo6['high'].iloc[-6]:
    elif (resumo6['high'].iloc[-2] < resumo6['high'].iloc[-3] < resumo6['high'].iloc[-4] > resumo6['high'].iloc[-5] > resumo6['high'].iloc[-6]) & (resumo6['MA21'].iloc[-2] < resumo6['MA50'].iloc[-2]) & (resumo6['MA50'].iloc[-2] < resumo6['MA200'].iloc[-2]):
        print(f'>>> {ativo}: VENDA')
        bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
        bot.sendMessage(-351556985, f'VENDA:..........{ativo}')
        #Valores()
        #print('')

    else:
        print(f'>>> {ativo}: Sem tendência definida <<<'.upper())
        #print('')

print('')
print('>>> FIM DA EXECUÇÃO! <<<') 