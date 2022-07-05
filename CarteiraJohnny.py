from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd

dados = open('C:\\Users\\johnny\\Documents\\Python Scripts\\VSCode\\dados.txt', 'r', encoding='utf-8')
leitura = dados.readlines()
usuario = leitura[0]
senha = leitura[1]
dados.close()

url = "https://br.investing.com/portfolio/?portfolioID=YmViNTFnMGQ3ZDsxNWQ4PQ%3D%3D"
tempo1 = 15
tempo2 = 10

'''
# NAVEGADOR FIREFOX DENTRO DO PC
option = Options()
option.headless = True
#driver = wb.Firefox(executable_path="C:\Program Files\geckodriver\geckodriver.exe", options=option)            # NAVEGADOR OFFLINE 
navegador = webdriver.Firefox(executable_path="C:\Program Files\geckodriver\geckodriver.exe")                   # NAVEGADOR ONLINE
navegador.get(url)

'''
# NAVEGADOR CHROME
option = Options()
option.headless = True
#navegador = webdriver.Chrome()                          # NAVEGADOR ON
navegador = webdriver.Chrome(options=option)            #NAVEGADOR OFF
navegador.get(url)
sleep(tempo2)

#clicar em I ACCEPT
accept = navegador.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
sleep(tempo2)


#usuário
usuarioName = navegador.find_element_by_xpath('//*[@id="loginFormUser_email"]')
usuarioName.click()
usuarioName.clear()
usuarioName.send_keys(usuario)

#senha
password = navegador.find_element_by_xpath('//*[@id="loginForm_password"]')
password.click()
password.clear()
password.send_keys(senha)
sleep(tempo2)

#clique login
cliquelogin = navegador.find_element_by_xpath('//*[@id="signup"]/a').click()
sleep(tempo2)
print('Entrando na página restrita')


#obter dados
navegador.get('https://br.investing.com/portfolio/?portfolioID=NjEyZGAyYztiMjo1ZDQyMw%3D%3D')
html = navegador.page_source

soup = BeautifulSoup (html, 'html.parser')
tabela = soup.find_all('table')[1]
tabelaDT = pd.read_html(str(tabela), decimal=',', thousands='.')[0]
#display(tabelaDT)
print('Obtendo dados')

navegador.close()

# Ajustando tabela
TabelaAnalise = tabelaDT[['Peso','Nome','Códigos','Qtd.','Méd. Preço','Preço atual','Valor Mercado','P/L Diário %','P/L Diário','% P/L líquido','P/L Líquido']]
TabelaAnalise = TabelaAnalise.sort_values(by='P/L Líquido',ascending=True)
#print(TabelaAnalise)

#A partir da tabela, obtendo lista dos ativos de Johnny
lista2 = tabelaDT.Códigos.tolist()

listaAnalise = []
for item in lista2:
    item_SA = item + '.SA'
    listaAnalise.append(item_SA)

print('Dados Disponíveis')
#print(listaAnalise)
