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
if not mt5.initialize(login=4999473749, server="MetaQuotes-Demo", password="elf4lnbx"):
    print("initialize() failed, error code =",mt5.last_error())
    quit()
    
def run():
    # CRIAÇÃO DAS ORDENS ABERTURA E FECHAMENTO
    # DOLAR ()
    #symbol = "EURUSD"
    #symbol = "WDOF22"
    symbol = "GBPUSD"
    item = symbol
    ativo = symbol

    print(symbol)

    
    # CRIAÇÃO DOS CÁLCULOS (MÉDIAS)
    timezone = pytz.timezone("Etc/UTC")
    utc_from = datetime(2021, 12, 28, tzinfo=timezone)
    rates = mt5.copy_rates_from(item, mt5.TIMEFRAME_M5, utc_from, 113)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
    resumo = rates_frame[['time','open','close','spread']]
    #resumo

    # SETUP 42.8
    QDoisMME = resumo['close'].ewm(span=42).mean() 
    OitoMME = resumo['close'].ewm(span=8).mean()

    resumo.insert(loc=4,column='MME 42',value=QDoisMME)
    resumo.insert(loc=5,column='MME 8',value=OitoMME)


    # MONITORAMENTO
    resumo['flag'] = ''
    resumo['sinal'] = ''

    for i in range (1, len(resumo)):
        if resumo['MME 42'][i] < resumo['MME 8'][i]:
            resumo['flag'][i] = 'COMPRA'
        else:
            resumo['flag'][i] = 'VENDA'

    for x in range(1,len(resumo)):
        if resumo['flag'][x] == resumo['flag'][x-1]:
            resumo['sinal'][x] = ''
        else:
            resumo['sinal'][x] = 'sinal'

    flag = resumo['flag'].iloc[-1]


    # LÓGICA DE EXECUCAO

    # MENSAGEM NA MUDANÇA DE CONDICAO
    if resumo['sinal'].iloc[-1] == 'sinal':
        bot = telepot.Bot('1852343442:AAEBBS1NjjFRIqt-XTbb3rzRxipvk8ZqI5I')
        bot.sendMessage(-351556985, f'ATENÇÃO! MUDANÇA DE STATUS: >> {item} - {flag} <<')
        print('Dados encontrados e enviados via Telegram'.upper())

    print(resumo.tail())
    print('')
    print('SCRIPT EXECUTADO COM SUCESSO. AGUARDANDO PRÓXIMA VARREDURA!')
    print('')

while True:
    run()
    time.sleep(300)