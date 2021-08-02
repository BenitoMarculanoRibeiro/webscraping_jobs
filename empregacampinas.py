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
    host='127.0.0.1',
    user='root',
    database='vagas',
    cursorclass=pymysql.cursors.DictCursor
)

status = True
cont = 0
limit = 3
while(status):
    try:
        url = 'https://empregacampinas.com.br/categoria/vaga/page/1'
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        for page in range(int(soup.find('span', class_='pages').text.split('de ')[1].replace('.', ''))):
            try:
                url = 'https://empregacampinas.com.br/categoria/vaga/page/' + \
                    str(page)
                soup = BeautifulSoup(requests.get(url).text, 'html.parser')
                teste = soup.find_all('a', class_="thumbnail")
                if(len(teste) == 0):
                    print(soup.prettify())
                    status = False
                    break

                for j in teste:
                    link = str(j['href'])
                    # Verifica se a vaga já exite no banco
                    mycursor = con.cursor()
                    sql = "SELECT COUNT(*) AS cont FROM vagas WHERE `link` LIKE %s"
                    mycursor.execute(sql, link)
                    myresult = mycursor.fetchone()
                    # Se não exite ele adicona
                    if(("https://empregacampinas.com.br" in str(j['href'])) and (myresult['cont'] == 0)):
                        print('Nova vaga: '+str(cont) +
                              ' - Data: ' + str(datetime.today()))
                        link = j['href']
                        l = BeautifulSoup(requests.get(link).text, 'html.parser').find(
                            'div', class_="conteudo-vaga")
                        titulo = l.find('h1').text
                        if(len(titulo.split("/")) > 3):
                            cidade = str(titulo.split(
                                "/")[1]) + " / "+str(titulo.split("/")[2])
                        else:
                            cidade = str(titulo.split("/")[1])
                        descricao = l.find('p').text
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
                #status = False
                print("Erro: ", e)
    except Exception as e:
        #status = False
        print("Erro: ", e)
