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

def cria_Objeto_JSON(produto, cor, tamanho, valor, img_link):
    x = {"produto": produto, "cor": cor, "tamanho": tamanho,
         "valor": valor, "img_link": img_link}
    return x


def criaJSON(objetos):
    y = {"produtos": objetos}
    return y

for i in range(1):
    
    try:
        url = 'https://br.indeed.com/empregos?l=Chile&start='+str(i*10)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        teste = soup.find_all('div', class_="job_seen_beacon")
        print(len(teste))
        #titulo_da_vaga
        #cidade
        #descrição
        #link_de_acesso
        #for j in teste:
        #    print(j.prettify())
        #    print("\n\n\n")
        print(teste[0].prettify())
        print("\n\n\n")
        #titulo_da_vaga
        #cidade
        #descrição
        #link_de_acesso
        print(str(url) + "  |||  " + str(r.status_code))

    except Exception as e:
        print("Servidor indisponível. Erro:", e)
        #print(soup.prettify())
        #arquivo = open('index.html', 'w')
        #arquivo.write(soup.prettify())
