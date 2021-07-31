import pymysql
#import json
import requests
from bs4 import BeautifulSoup
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


con = pymysql.connect(host='127.0.0.1', user='root',
                      database='vagas', cursorclass=pymysql.cursors.DictCursor)
i = 0
status = True
while(status):
    try:
        url = 'https://br.indeed.com/jobs?q=&l=Vitória%2C+ES&start=' + str(i)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        teste = soup.find_all('a', class_="tapItem")
        if(len(teste) == 0):
            print(soup.prettify())
            status = False
            break
        vagas = []
        for j in teste:
            ''' 
            titulo = j.find('a', class_="vagaTitle").find(
                'h2').text.replace("\n", "").rstrip("\r                            ")
            cidade = j.find('p', class_="location2").findAll('span')[
                1]['title']
            link = str(j.find('a', class_="vagaTitle")['href'])
            descricao = BeautifulSoup(requests.get(link).text, 'html.parser').find(
                'div', class_="advisor-vacancy-content")
            descricao = descricao.find('ol', class_="descriptionItems").text
            '''
            
            titulo = j.find(
                'h2', class_="jobTitle").findAll('span')[-1].text
            cidade = j.find('div', class_="companyLocation").text
            link = "https://br.indeed.com"+str(j['href'])
            descricao = BeautifulSoup(requests.get(link).text, 'html.parser').find(
                'div', class_="jobsearch-jobDescriptionText").text
            val = (str(titulo), str(link), str(cidade), str(descricao))
            vagas.append(val)

        with con.cursor() as c:
            sql = "INSERT INTO `vagas` (`id`, `titulo`, `link`, `cidade`, `descricao`) VALUES (NULL, %s, %s,%s, %s);"
            c.executemany(sql, vagas)
        con.commit()
        #print(2)
            #vagas.append(cria_Objeto_JSON(titulo, cidade, descrição, link))
        #with open('dados_indeed.json', 'w', encoding='utf8') as json_file:
        #    json.dump(criaJSON(vagas), json_file, ensure_ascii=False)
        print(i/10)
        i += 10
    except Exception as e:
        status = False
        print("Acabou. Erro:", e)

#print(criaJSON(vagas))
#with open('indeed.json', 'w', encoding='utf8') as json_file:
 #   json.dump(criaJSON(vagas), json_file, ensure_ascii=False)
