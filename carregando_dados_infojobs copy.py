import pymysql
from datetime import datetime
#import json
import requests
from bs4 import BeautifulSoup


def cria_Objeto_JSON(titulo, cidade, descricao, link):
    x = {"titulo": titulo, "cidade": cidade,
         "descricao": descricao, "link": link}
    return x


def criaJSON(objetos):
    y = {"vagas": objetos}
    return y


con = pymysql.connect(host='127.0.0.1', user='root',
                      database='vagas', cursorclass=pymysql.cursors.DictCursor)
i = 0
status = True
cont = 0

while(status):
    try:
        url = 'https://www.infojobs.com.br/empregos.aspx?Page=' + str(i)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        teste = soup.find_all('div', class_="element-vaga")
        if(len(teste) == 0):
            print(soup.prettify())
            status = False
            break
        # for j in range(int(3)):
        vagas = []
        for j in teste:
            titulo = j.find('a', class_="vagaTitle").find('h2').text.replace(
                "\n", "").rstrip("\r                            ")
            cidade = j.find('p', class_="location2").findAll(
                'span')[1]['title']
            link = str(j.find('a', class_="vagaTitle")['href'])
            # Verifica se a vaga já exite no banco
            mycursor = con.cursor()
            sql = "SELECT COUNT(*) AS cont FROM vagas WHERE `link` LIKE %s"
            mycursor.execute(sql, link)
            myresult = mycursor.fetchone()
            # Se não exite ele adicona
            if(myresult['cont'] == 0):
                print('Nova vaga: '+str(cont) +
                      ' - Data: ' + str(datetime.today()))
                descricao = BeautifulSoup(requests.get(link).text, 'html.parser').find(
                    'div', class_="advisor-vacancy-content")
                descricao = descricao.find(
                    'ol', class_="descriptionItems").text
                vaga = (str(titulo), str(link), str(cidade), str(descricao))
                with con.cursor() as c:
                    sql = "INSERT INTO `vagas` (`id`, `titulo`, `link`, `cidade`, `descricao`) VALUES (NULL, %s, %s,%s, %s);"
                    c.execute(sql, vaga)
                con.commit()
                cont += 1
        i += 1
    except Exception as e:
        #status = False
        print(e)
con.close()
