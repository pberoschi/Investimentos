import pandas as pd
from bs4 import BeautifulSoup
import yfinance as yf
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options

import compravenda
import MaisNegociadas
#import CarteiraJohnny


from flask import Flask, render_template, request
app = Flask(__name__) 

@app.route('/precos')
def my_form():
    return render_template('precos.html')

@app.route('/precos', methods=['POST'])
def my_form_post():
    text = request.form['text']
    ticker = text.upper() + '.SA'
 
    dia = yf.Ticker(ticker)
    base = dia.history(period='1d', interval='1m')
    #MEDIAS do dia
    mediaDia = base[['Low','High']].mean()
    mediaDia2 = base[['Low','High']]
    #MEDIA da ultima hora
    mediaHora1 = base[['Low','High']].tail(60)
    mediaHora = mediaHora1.mean()
    #MEDIA 15 minutos
    media15_1 = base[['Low','High']].tail(15)
    media15 = media15_1.mean()

    return render_template('precos.html', mediaDia=mediaDia, mediaHora1=mediaHora1, media15=media15)


@app.route('/mais_negociadas')
def MaisNegoc():
    dicMaisNegociadas = MaisNegociadas.resumoMN
    return render_template('MaisNegociadas.html', dados2=dicMaisNegociadas)


@app.route('/compravenda')
def compra_venda():
    lista = compravenda.dicionario2
    return render_template('compravenda.html', lista=lista)

#adicionando comentários na máquina WinHouse
#outra modificação

app.run(debug=True)
