#from selenium import webdriver
from time import sleep
import pandas as pd
import yfinance as yf
#pd.options.mode.chained_assignment = None
import ativos


#ticker = ativos.tickerteste
ticker = ativos.ativosJohnny
listaativos = [] 

# ANALISE DE CADA PAPEL
for x in ticker:
    dia2 = yf.Ticker(x)
    Dia = dia2.history(period='1d', interval='5m').tail(1)
    mediaporMinuto = dia2.history(period='1d', interval='1m')
    mediaporMinuto = mediaporMinuto['Close'].mean()
    mediaporMinuto = round(mediaporMinuto, 3)
    Ano = yf.download(x, period='1y')
    #print(x)     
    #ANO: criando coluna Data e transferindo valores
    Ano.insert(loc=0, column='DataMain', value=Ano.index)
    #remove a ultima data
    removedata = Ano.loc[(Ano['DataMain']==pd.to_datetime('today').normalize())]
    Ano = Ano.drop(removedata.index)
    #DIA: criando coluna Data e transferindo valores
    Dia.insert(loc=0, column='DataMain', value=Dia.index)
    #unindo os periodos
    Resumo = Ano.append(Dia)
    #ajuste da data
    Resumo['DataMain'] = pd.to_datetime(Resumo['DataMain'], utc=True).dt.date
    #resumindo as colunas desejadas (data e fechamento)
    ResumoEnd = Resumo[['DataMain', 'Close']]
    #calculo MACD
    rapidoMME = ResumoEnd.Close.ewm(span=12).mean()
    lentaMME = ResumoEnd.Close.ewm(span=26).mean()
    MACD = rapidoMME - lentaMME
    Sinal = MACD.ewm(span=9).mean()
    ResumoEnd['MACD'] = MACD
    ResumoEnd['Sinal'] = Sinal
    #ajuste index e retira data; coloca data como index
    ResumoEnd = ResumoEnd.set_index(pd.DatetimeIndex(ResumoEnd['DataMain'].values))
    ResumoEnd = ResumoEnd.drop('DataMain', 1)
    # criar código para verificar a compra ou venda
    ResumoEnd['flag'] = ''
    ResumoEnd['preco_compra'] = ''
    ResumoEnd['preco_venda'] = ''
    for i in range (1, len(ResumoEnd.Sinal)):
        if ResumoEnd['MACD'][i] > ResumoEnd['Sinal'][i]:
            if ResumoEnd['flag'][i-1] == 'C':
                ResumoEnd['flag'][i] = 'C'
            else:
                ResumoEnd['flag'][i] = 'C'
                ResumoEnd['preco_compra'][i] = ResumoEnd['Close'][i]
                
        elif ResumoEnd['MACD'][i] < ResumoEnd['Sinal'][i]:
            if ResumoEnd['flag'][i-1] == 'V':
                ResumoEnd['flag'][i] = 'V'
            else:
                ResumoEnd['flag'][i] = 'V'
                ResumoEnd['preco_venda'][i] = ResumoEnd['Close'][i]
            
    hoje = ResumoEnd.flag[-1]
    ontem = ResumoEnd.flag[-2]
    flag = hoje
    #ticker2 = x[0:-3]
    #site = f'https://www.google.com/search?q={ticker2}&rlz=1C1EJFC_enBR915BR916&oq={ticker2}&aqs=chrome..69i57j0l5j0i10i433j69i60.4408j0j7&sourceid=chrome&ie=UTF-8'
    #preco_fechamento = round(ResumoEnd.Close.tail(1)[-1],2)
    #msg = f'{ticker2}  \n>>> {flag} <<< \nPreço de Fechamento: {preco_fechamento} \nPreço Médio/Dia: {mediaporMinuto} \n\nTotal de ações analisadas: {len(ticker)}\n {site}'
    
    dicativos = {
        'ATIVO': x,
        'FLAG': flag
    }

    listaativos.append(dicativos)

resumo = pd.DataFrame(listaativos)
dicionario2 = resumo.to_dict('records')

#print(dicionario2)
print('Processo Finalizado; Dicionário Pronto')