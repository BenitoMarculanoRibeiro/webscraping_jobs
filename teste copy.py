from datetime import datetime
from bs4 import BeautifulSoup
from lxml import etree
import pymysql
import requests

con = pymysql.connect(
    host='remotemysql.com',
    user='aEe2LdBimG', password='SvfgdVTUw5',
    database='aEe2LdBimG',
    cursorclass=pymysql.cursors.DictCursor
)

'''URL = "https://en.wikipedia.org/wiki/Nike,_Inc."
url = f'https://www.trabalhabrasil.com.br/api/v1.0/Job/List?idFuncao=0&idCidade=0&pagina=2&pesquisa=&ordenacao=1&idUsuario=&flgHomeOffice=false'
'''
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'pt-br, pt;q=0.5'})
'''
pages = requests.get(url, headers=HEADERS).json()

print(str(pages[0]))
for page in pages:
    titulo = page['tt']
    link = f'https://www.trabalhabrasil.com.br/{page["u"]}'
    cidade = page['uf']
    descricao = page['d']
    print(titulo, link, cidade, descricao)
    mycursor = con.cursor()
    sql = "SELECT COUNT(*) AS cont FROM vagas WHERE `link` LIKE %s"
    mycursor.execute(sql, link)
    myresult = mycursor.fetchone()
    if(myresult['cont'] == 0):
        vaga = (str(titulo), str(link),str(cidade), str(descricao))
        with con.cursor() as c:
                        sql = "INSERT INTO `vagas` (`id`, `titulo`, `link`, `cidade`, `descricao`) VALUES (NULL, %s, %s,%s, %s);"
                        c.execute(sql, vaga)
                        con.commit()'''


while(True):
    pagina = 2
    status = True
    cont = 0
    while(status):
        try:
            url = f'https://www.trabalhabrasil.com.br/api/v1.0/Job/List?idFuncao=0&idCidade=0&pagina={str(pagina)}&pesquisa=&ordenacao=1&idUsuario=&flgHomeOffice=false'
            pages = requests.get(url, headers=HEADERS).json()
            # print(teste)
            if(None != pages):
                vagas = []
                # Como na pagina de pesquisa não aparece toda a descricao, tem que entrar em cada vaga para ler se exite.
                for page in pages:
                    titulo = page['tt']
                    link = f'https://www.trabalhabrasil.com.br/{page["u"]}'
                    cidade = page['uf']
                    descricao = page['d']
                    # Verifica se a vaga já exite no banco
                    mycursor = con.cursor()
                    sql = "SELECT COUNT(*) AS cont FROM vagas WHERE `link` LIKE %s"
                    mycursor.execute(sql, link)
                    myresult = mycursor.fetchone()
                    print(myresult, link)
                    # Se não exite ele adicona
                    if(myresult['cont'] == 0):
                        print('Nova vaga: '+str(cont) +
                              ' - Data: ' + str(datetime.today()))
                        vaga = (str(titulo), str(link),
                                str(cidade), str(descricao))
                        with con.cursor() as c:
                            sql = "INSERT INTO `vagas` (`id`, `titulo`, `link`, `cidade`, `descricao`) VALUES (NULL, %s, %s,%s, %s);"
                            c.execute(sql, vaga)
                        con.commit()
                        cont += 1
                pagina += 1
                print("Pagina: " + str(pagina))
        except Exception as e:
            status = False
            print("Erro: ", e)
