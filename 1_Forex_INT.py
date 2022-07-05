from datetime import datetime
import MetaTrader5 as mt5
import time
import telepot

agora = datetime.now()

print(f'Buscando dados...{agora}')

# importamos o módulo pandas para exibir os dados recebidos na forma de uma tabela
import pandas as pd
pd.set_option('display.max_columns', 500) # número de colunas
pd.set_option('display.width', 1500)      # largura máxima da tabela

# importamos o módulo pytz para trabalhar com o fuso horário
import pytz

# estabelecemos a conexão ao MetaTrader 5
#if not mt5.initialize(login=50717088, server="ICMarketsSC-Demo", password="2DLJdDev"):
if not mt5.initialize(login=54679378, server="MetaQuotes-Demo", password="hz7ulfri"):
#if not mt5.initialize(login=1002947504, server="ClearInvestimentos-CLEAR", password="Joh0516"):
    print("initialize() failed, error code =",mt5.last_error())
    quit()

ativo = ["EURUSD","GBPUSD","USDJPY","USDCHF","USDCAD","AUDUSD","NZDUSD"]

for item in ativo:
    # definimos o fuso horário como UTC
    timezone = pytz.timezone("Etc/UTC")

    # criamos o objeto datetime no fuso horário UTC para que não seja aplicado o deslocamento do fuso horário local
    utc_from = datetime(2021, 11, 26, tzinfo=timezone)

    # recebemos 10 barras de EURUSD H4 a partir de 01/10/2019 no fuso horário UTC
    #rates = mt5.copy_rates_from(item, mt5.TIMEFRAME_M5, utc_from, 100)
    rates = mt5.copy_rates_from(item, mt5.TIMEFRAME_M5, utc_from, 150)


    # a partir dos dados recebidos criamos o DataFrame
    rates_frame = pd.DataFrame(rates)
    # convertemos o tempo em segundos no formato datetime
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')


    resumo = rates_frame[['time','open','close','spread']]
    #resumo

    #Criar Sinais de compra e venda
    openMME = resumo['open'].ewm(span=3).mean()      #cor: VERDE(3)
    closeMME = resumo['close'].ewm(span=30).mean()   #cor: VERMELHA(30)

    resumo.insert(loc=4,column='MMEopen',value=openMME)
    resumo.insert(loc=5,column='MMEclose',value=closeMME)
    print(resumo.tail())

    #def monitoramento():
    pd.options.mode.chained_assignment = None

    resumo['flag'] = ''
    resumo['sinal'] = ''

    for i in range (1, len(resumo)):
        if resumo['MMEopen'][i] > resumo['MMEclose'][i]:
            resumo['flag'][i] = 'VENDA'
        else:
            resumo['flag'][i] = 'COMPRA'

    for x in range(1,len(resumo)):
        if resumo['flag'][x] == resumo['flag'][x-1]:
            resumo['sinal'][x] = ''
        else:
            resumo['sinal'][x] = 'sinal'
            
    flag = resumo['flag'].iloc[-1]
    if resumo['sinal'].iloc[-1] == 'sinal':
        bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
        bot.sendMessage(-351556985, f'ATENÇÃO! MUDANÇA DE STATUS: >> {item} - {flag} <<')
        print('Dados encontrados e enviados via Telegram'.upper())
        time.sleep(3)
    #print(ativo)
    #print(resumo.tail())

print('Script executado com sucesso. Fechando o programa...'.upper())
time.sleep(5)






