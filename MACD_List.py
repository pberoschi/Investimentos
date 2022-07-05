import yfinance as yf
import pandas as pd
import ativos
 
pd.options.mode.chained_assignment = None 
 
tickeres = ativos.tickerteste

for ticker in tickeres:
  df_itub = yf.download(ticker, period='1y')
  itub = yf.Ticker(ticker)
  Dia = itub.history(period='1d', interval='5m').tail(1)
  Ano = yf.download(ticker, period='1y')
  Ano.insert(loc=0, column='DataMain', value=Ano.index)
  removedata = Ano.loc[(Ano['DataMain']==pd.to_datetime('today').normalize())]
  Ano = Ano.drop(removedata.index)
  Dia.insert(loc=0, column='DataMain', value=Dia.index)
  Resumo = Ano.append(Dia)
  Resumo['DataMain'] = pd.to_datetime(Resumo['DataMain'], utc=True).dt.date
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
  ResumoEnd['compra'] = ''
  ResumoEnd['venda'] = ''
 
  for i in range (1, len(ResumoEnd.Sinal)):
    if ResumoEnd['MACD'][i] > ResumoEnd['Sinal'][i]:
      if ResumoEnd['flag'][i-1] == 'C':
        ResumoEnd['flag'][i] = 'C'
      else:
        ResumoEnd['flag'][i] = 'C'
        ResumoEnd['compra'][i] = ResumoEnd['Close'][i]
 
    elif ResumoEnd['MACD'][i] < ResumoEnd['Sinal'][i]:
      if ResumoEnd['flag'][i-1] == 'V':
        ResumoEnd['flag'][i] = 'V'
      else:
        ResumoEnd['flag'][i] = 'V'
        ResumoEnd['venda'][i] = ResumoEnd['Close'][i]
    
  print(ResumoEnd.tail(1))