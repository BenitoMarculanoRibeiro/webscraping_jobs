import time
from datetime import datetime
import pymysql
import requests
from bs4 import BeautifulSoup


def cria_Objeto_JSON(produto, cor, tamanho, valor, img_link):
    x = {"produto": produto, "cor": cor, "tamanho": tamanho,
         "valor": valor, "img_link": img_link}
    return x


def criaJSON(objetos):
    y = {"produtos": objetos}
    return y


con = pymysql.connect(
    host='remotemysql.com',
    user='aEe2LdBimG', password='SvfgdVTUw5',
    database='aEe2LdBimG',
    cursorclass=pymysql.cursors.DictCursor
)
while(True):
    page = 1
    status = True
    cont = 0
    while(status):
        try:
            url = 'https://www.catho.com.br/vagas/?page=' + str(page)
            soup = BeautifulSoup(requests.get(url).text, 'html.parser')
            teste = soup.find('ul', class_="gtm-class").find_all('li')
            # print(teste)
            if(None != teste):

                '''
                if(len(teste) == 0):
                    print('captcha')
                    time.sleep(60)
                    # print(soup.prettify())
                    #status = False
                    pass
                '''
                vagas = []
                # Como na pagina de pesquisa não aparece toda a descricao, tem que entrar em cada vaga para ler se exite.
                for j in teste:
                    link = str(j['data-gtm-page']).split('//')
                    link = str(link[0])+'//'+str(link[1])
                    # Verifica se a vaga já exite no banco
                    mycursor = con.cursor()
                    sql = "SELECT COUNT(*) AS cont FROM vagas WHERE `link` LIKE %s"
                    mycursor.execute(sql, link)
                    myresult = mycursor.fetchone()
                    # Se não exite ele adicona
                    if(myresult['cont'] == 0):
                        print('Nova vaga: '+str(cont) +
                              ' - Data: ' + str(datetime.today()))
                        novaPage = BeautifulSoup(
                            requests.get(link).text, 'html.parser')
                        titulo = novaPage.find('h2').find('a').text
                        cidade = novaPage.find(
                            'div', class_="cidades").text.split('(')[0]
                        descricao = novaPage.find(
                            'span', class_="job-description").text
                        vaga = (str(titulo), str(link),
                                str(cidade), str(descricao))
                        with con.cursor() as c:
                            sql = "INSERT INTO `vagas` (`id`, `titulo`, `link`, `cidade`, `descricao`) VALUES (NULL, %s, %s,%s, %s);"
                            c.execute(sql, vaga)
                        con.commit()
                        cont += 1
                page += 1
                print("Pagina: " + str(page))
        except Exception as e:
            status = False
            print("Erro: ", e)
