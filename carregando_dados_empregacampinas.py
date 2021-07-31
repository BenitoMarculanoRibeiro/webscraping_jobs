import MySQLdb
import json
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


i = 0
status = True
vagas = []
notvagas = []
while(status):
    try:
        url = 'https://empregacampinas.com.br/categoria/vaga/page/' + str(i)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        teste = soup.find_all('a', class_="thumbnail")
        
        if(len(teste) == 0):
            print(soup.prettify())
            status = False
            break
        for j in teste:
            if("https://empregacampinas.com.br" in str(j['href'])):
                link = j['href']
                print(link)
                l = BeautifulSoup(requests.get(link).text, 'html.parser').find(
                    'div', class_="conteudo-vaga")
                titulo = l.find('h1').text
                if(len(titulo.split("/")) > 3):
                    cidade = str(titulo.split(
                        "/")[1]) + " / "+str(titulo.split("/")[2])
                else:
                    cidade = str(titulo.split("/")[1])
                descricao = l.find('p').text
                vagas.append(cria_Objeto_JSON(titulo,
                                            cidade, descricao, link))
                print(vagas[-1])
                print("\n\n")
        print(i)
        i += 1
        with open('dados_empregacampinas.json', 'w', encoding='utf8') as json_file:
            json.dump(criaJSON(vagas), json_file, ensure_ascii=False)
        
    except Exception as e:
        status = False
        print("Acabou. Erro:", e)
#print(criaJSON(vagas))
with open('dados_empregacampinas.json', 'w', encoding='utf8') as json_file:
    json.dump(criaJSON(vagas), json_file, ensure_ascii=False)
# with open('dados_infojobs.json', 'w', encoding='utf8') as json_file:
#    json.dumps(criaJSON(vagas), json_file, ensure_ascii=False)
