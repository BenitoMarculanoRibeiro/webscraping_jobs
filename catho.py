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
                    print(myresult, link)
                    # Se não exite ele adicona em uma lista temporaria
                    if(myresult['cont'] == 0):
                        print('Nova vaga: '+str(cont) + ' - Data: ' + str(datetime.today()))
                        novaPage = BeautifulSoup(
                            requests.get(link).text, 'html.parser')
                        titulo = novaPage.find('h2').find('a').text
                        cidade = novaPage.find(
                            'div', class_="cidades").text.split('(')[0]
                        descricao = novaPage.find(
                            'span', class_="job-description").text
                        vagas.append((str(titulo), str(link), str(cidade), str(descricao), str(link)))
                # Addiciona a lista temporaria no banco
                if len(vagas) > 0:
                    with con.cursor() as c:
                        sql = "INSERT INTO `vagas` (`titulo`, `link`, `cidade`, `descricao`) SELECT %s, %s, %s, %s WHERE NOT EXISTS(SELECT 1 FROM `vagas` WHERE `link` = %s)"
                        c.executemany(sql, vagas)
                        con.commit()
                        print(c.rowcount, "record(s) inserted.")
                cont += 1
                page += 1
                print("Pagina: " + str(page))
        except Exception as e:
            status = False
            print("Erro: ", e)
