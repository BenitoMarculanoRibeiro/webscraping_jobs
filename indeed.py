from selenium import webdriver
import pymysql
from datetime import datetime
import time
#import json
import requests
from bs4 import BeautifulSoup

con = pymysql.connect(
    host='127.0.0.1',
    user='root',
    database='vagas',
    cursorclass=pymysql.cursors.DictCursor
)
page = 0
status = True
cont = 0

# while(status):
try:
    # Criar instância do navegador
    firefox = webdriver.Firefox()

    # Abrir a página do Python Club
    firefox.get(
        'https://br.indeed.com/empregos?l=Brasil&start=' + str(page))
    links = firefox.find_elements_by_css_selector('.tapItem')
    for link in links:
        print(link.get_attribute('href'))
    # Seleciono todos os elementos que possuem a class post
    # firefox.find_element_by_xpath('//*[@id="checkbox"]').click()
    # Para cada post printar as informações

    # Fechar navegador
    firefox.quit()
except Exception as e:
    #status = False
    print("Erro: ", e)
