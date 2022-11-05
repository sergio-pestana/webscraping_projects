from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import yfinance as yf
import pandas_datareader.data as web
import seaborn as sns
import matplotlib.pyplot as plt


general_url = 'https://br.advfn.com/'

page = requests.get(url=general_url)
soup = BeautifulSoup(page.content, 'lxml')

# dataframe dos valores das princ bolsas internacionais
bolsas_indx = soup.find('div', attrs={'id':'indices'}).table
table_bolsas = pd.read_html(str(bolsas_indx), decimal=',', thousands='.')[0].dropna(axis=1).rename(columns={'Unnamed: 0':'Índice'})

# dataframe do cambio
cambio_html = soup.find('div', attrs={'class':'bx-sidebar-container'}).table
table_cambio = pd.read_html(str(cambio_html), decimal=',', thousands='.')[0].dropna(axis=1).rename(columns={'Nome':'Câmbio Real'})


# Ranking de Ações Bovespa

ranking = soup.findAll('div', attrs={'class':'col-ranking'})

## Mariores altas
ranking_maiores = ranking[0].table
table_maiores = pd.read_html(str(ranking_maiores), decimal=',', thousands='.')[0].dropna(axis=1)

## Maiores Baixas
ranking_baixas = ranking[1].table
table_baixas = pd.read_html(str(ranking_baixas), decimal=',', thousands='.')[0].dropna(axis=1)

## Maior volume
ranking_vol = ranking[2].table
table_vol = pd.read_html(str(ranking_vol), decimal=',', thousands='.')[0].dropna(axis=1)


news = 'https://br.advfn.com/noticias/carteira-recomendada'
news_page = requests.get(url=news)
sp = BeautifulSoup(news_page.content, 'lxml')
content = sp.findAll('div', class_='col-lg-3 col-md-3 col-sm-12 col-xs-12 story')

# ultimas noticias
text_noticias = []
for i in range(4):
    title = content[i].find('h3', class_='post-title').text.replace('\n','')
    link = content[i].find('h3', class_='post-title').a['href']
    texto = "<p>"+str(title) + " -> <a href=" + link + ">link</a></p>"
    
    text_noticias.append(texto)


# mandando para o MS Teams

import pymsteams
import time, datetime

date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
teams_conn = 'https://outlook.office.com/webhook/5e36e63c-abda-4afb-9a01-97da93bd0091@945c199a-83a2-4e80-9f8c-5a91be5752dd/IncomingWebhook/e75aa2266b644caabab2a88b34389b70/0c8491b1-80f0-4d38-b186-29b57dfe0f07'

msg = pymsteams.connectorcard(teams_conn)
msg.color('<#FF5733>')
msg.title('Finance Report')

txt = """<p>Bom dia @general ! Ultima atualizacao em: {0}</p><p><br></p><p>Índices de Bolsas</p><p><br></p><p>{1}</p></p><p><br>
<p>Taxas de Câmbio</p><p><br></p><p>{2}</p><p><br></p>>>> Maiores Altas<p>{3}</p>
<p><br></p>
<p>>> Maiores Baixas</p>
<p>{4}</p>
<p><br></p>
<p>Maiores Volume</p>
<p>{5}</p>
<p><br></p><p>Últimos artigos sobre Carteira Recomendada</p><p><br></p>
<p>{6}</p>""".format(date, table_bolsas.to_html(index=False), table_cambio.to_html(index=False), table_maiores.to_html(index=False),
        table_baixas.to_html(index=False),table_vol.to_html(index=False),str(text_noticias).replace(',',''))

msg.text(txt)

msg.addLinkButton("Últimas Notícias - Valor Econ.", 'https://valor.globo.com/ultimas-noticias/')

msg.send()

print('SENT!')
