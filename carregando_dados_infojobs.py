import pymysql
#import json
import requests
from bs4 import BeautifulSoup
from lxml import html

# empregacampinas = https://empregacampinas.com.br/categoria/vaga/page/2

# infojobs  = https://www.infojobs.com.br/empregos.aspx?Page=2

# catho = https://www.catho.com.br/vagas/?page=2

# Mais complicado
# indeed = https://br.indeed.com/jobs?q=&l=Chile&start=20

# Muito mais complicado
# trabalhabrasil = 'https://www.trabalhabrasil.com.br/api/v1.0/Job/List?idFuncao=0&idCidade='+str(id_cidade)+'&pagina='+str(pagina)+'&pesquisa=&ordenacao=1&idUsuario='
# retorna json



def cria_Objeto_JSON(titulo, cidade, descricao, link):
    x = {"titulo": titulo, "cidade": cidade,
         "descricao": descricao, "link": link}
    return x


def criaJSON(objetos):
    y = {"vagas": objetos}
    return y


con = pymysql.connect(
    host='remotemysql.com',
    user='aEe2LdBimG', password='SvfgdVTUw5',
    database='aEe2LdBimG',
    cursorclass=pymysql.cursors.DictCursor
)
i = 0
status = True

while(status):
    try:
        url = 'https://www.infojobs.com.br/empregos-em-sao-paulo.aspx?page=' + str(i)
        r = requests.get(url)
        #soup = BeautifulSoup(r.text, 'html.parser')
        #teste = soup.find_all('div', id_="filterSideBar")
        tree = html.fromstring(r.content)
        teste = tree.xpath("//div[@id='filterSideBar']/div")
        if(len(teste) == 0):
            #print(soup.prettify())
            print('break')
            status = False
            break
        print('pass', len(teste))
        # for j in range(int(3)):
        vagas = []
        for j in teste:
            titulo = j.find('a', class_="vagaTitle").find(
                'h2').text.replace("\n", "").rstrip("\r                            ")
            cidade = j.find('p', class_="location2").findAll('span')[
                1]['title']
            link = str(j.find('a', class_="vagaTitle")['href'])
            descricao = BeautifulSoup(requests.get(link).text, 'html.parser').find(
                'div', class_="advisor-vacancy-content")
            descricao = descricao.find('ol', class_="descriptionItems").text
            vagas.append({titulo, link, cidade, descricao})
            print(1)
        with con.cursor() as c:
            sql = "INSERT INTO `vagas` (`id`, `titulo`, `link`, `cidade`, `descricao`) VALUES (NULL, %s, %s,%s, %s);"
            c.execute(sql, vagas)
        con.commit()
        print(2)
        # print(i)
        # with open('dados_infojobs.json', 'w', encoding='utf8') as json_file:
            #json.dump(criaJSON(vagas), json_file, ensure_ascii=False)
        i += 1
    except Exception as e:
        status = False
        print(e)
#print(criaJSON(vagas))
#with open('dados_infojobss.json', 'w', encoding='utf8') as json_file:
 #   json.dump(criaJSON(vagas), json_file, ensure_ascii=False)
# with open('dados_infojobs.json', 'w', encoding='utf8') as json_file:
#    json.dumps(criaJSON(vagas), json_file, ensure_ascii=False)

con.close()
