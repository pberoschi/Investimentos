import pandas as pd
import yfinance as yf
 
def media1minuto():
  dia = yf.Ticker(ticker + '.SA')
  cinco1min = dia.history(period='1d', interval='1m')
  media1min = cinco1min['Close'].mean()
  final1min = round(media1min, 3)
  #print(f'Valor Médio: R$ {final1min} (por MINUTO)')
 
def media60minuto():
  dia = yf.Ticker(ticker + '.SA')
  cinco60min = dia.history(period='1d', interval='1h')
  media60min = cinco60min['Close'].mean()
  final60min = round(media60min, 2)
      #round(ResumoEnd.Close.tail(1)[-1],2)
  #print(f'Valor Médio: R$ {final60min} (por HORA)')
 
 
