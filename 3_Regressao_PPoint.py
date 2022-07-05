#!/usr/bin/env python
# coding: utf-8

# In[24]:


#https://github.com/alissonf216/Robo-Pivot-Point-Mt5-com-Python/blob/main/Pontos%20de%20pivo%20para%20Daytrade%20-%20simula%C3%A7%C3%A3o%20resultados%20.ipynb


import pandas as pd
from pandas_datareader import data as pdr
import numpy as np
import matplotlib.pyplot as plt
import yfinance
import warnings
get_ipython().run_line_magic('matplotlib', 'inline')
warnings.filterwarnings('ignore')


# In[25]:


ativo = yfinance.Ticker("itub4.SA")
df = ativo.history(interval="5m", period = "1d")

# buscando series historias outro jeito mais simples
#df = pdr.DataReader('itub4.SA',data_source='yahoo', start='2020-02-28', end = '2020-04-02');
#df.tail()


# In[26]:


df.iloc[-1].copy()


# In[27]:


df


# In[28]:


df['Pivot'] = (df['High'] + df['Low'] + df['Close'])/3
df['R1'] = 2*df['Pivot'] - df['Low']
df['S1'] = 2*df['Pivot'] - df['High']
df['R2'] = df['Pivot'] + (df['High'] - df['Low'])
df['S2'] = df['Pivot'] - (df['High'] - df['Low'])
df['R3'] = df['Pivot'] + 2*(df['High'] - df['Low'])
df['S3'] = df['Pivot'] - 2*(df['High'] - df['Low'])


# In[29]:


df.tail()


# In[30]:


#criando colulas vazias no data frema
df['Compra pivot'],df['Venda S1'],df['Acumulado'] = 'NaN','NaN','NaN'


# In[ ]:


#copiando dataframe para poder fazer os calculos
#dfcalc = df.copy()


# In[ ]:


#excluindo primeira linha do df para poder usar como inicio o comparador do outro df calc vou excluir apenas com um filtro
#df = df.loc[df.index > '2020-01-02']


# In[31]:


df


# In[ ]:


#renomedo colunas  codigo comentado para nao execultaR
##dfcalc = dfcalc.rename(columns={'Pivot': 'P-Pivot','S1':'S-S1'})


# In[ ]:


#Criando nova coluna inutil kkkkkkkk
###df['P-Pivot'] = 'NaN'


# In[ ]:


#testes = df['Pivot'][n]/df['Pivot'][n -1]


# In[ ]:


#testes


# In[ ]:



# testa dor de entrada de valor está correto!

#posicao = 4
#if df['High'][posicao]>df['Pivot'][posicao - 1]:
#    df['Compra pivot'][posicao] = df['Close'][posicao] - df['Pivot'][posicao - 1]
#else:
#    df['Compra pivot'][posicao] = 0


# In[ ]:


#n = 0
#while n<7:
#    df['Compra pivot'] = 'NaN';
 #   n = n +1;


# In[32]:


#criando valores de lucro na entrada comprando no Pivot
posicao = 0
while posicao<len(df['Pivot']):
    if df['High'][posicao]>df['Pivot'][posicao - 1]:
        df['Compra pivot'][posicao] = df['Close'][posicao] - df['Pivot'][posicao - 1]
    else:
        df['Compra pivot'][posicao] = 0
    posicao = posicao +1;


# In[33]:


#criando valores de lucro na entrada vendido na Primeiro Suporte
posicao = 0
while posicao<len(df['S1']):
    if df['Low'][posicao]<df['S1'][posicao - 1]:
        df['Venda S1'][posicao] = df['S1'][posicao - 1] - df['Close'][posicao]
    else:
        df['Venda S1'][posicao] = 0
    posicao = posicao +1;


# In[34]:


# SOMANDO SO RESULTADOS DOS GANHOS DAS ENTRADAS DE UM LOTE MINIMO DE 100 AÇOES- COMPRA E VENDA; 
for index, row in df.iterrows():
    df.loc[index,'Acumulado'] = (df.loc[index,'Compra pivot'] + df.loc[index,'Venda S1'])*100;


# In[35]:


df.tail()


# In[36]:


#excluindo primeira linha do df usar como inicio do comparador - SE NAO VC TEM UM ENTRADA COM O PARAMENTRO DO ULTIMO DIA
# E ISSO IRIA MUDAR O VALOR NA SOMATORIA TOTAL
df = df.loc[df.index > '2020-10-20 10:10:00']


# In[37]:


df


# In[38]:


np.cumsum(df['Acumulado']).plot(figsize = (16,8))


# In[ ]:




