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
#proxies = {'HTTP': '142.44.148.56:8080','SOCKS4': '192.99.176.117:5678'}
#resp = requests.get('http://example.com', proxies=proxies)
page = 0
status = True
cont = 0
s = requests.Session()
s.proxies = {
    "https": "http://115.75.1.184:8118",
    "https": "http://36.67.158.49:6530"
}
while(status):
    try:

        #r = s.get("http: // toscrape.com")
        #resp = requests.get('http://example.com', proxies=proxies)
        url = 'https://br.indeed.com/jobs?q=&l=Vitória%2C+ES&start=' + \
            str(page)
        soup = BeautifulSoup(s.get(url, timeout=10).text, 'html.parser')
        teste = soup.find_all('a', class_="tapItem")
        if(len(teste) == 0):
            print('captcha'+str(s.proxies))
            time.sleep(1)
            # print(soup.prettify())
            #status = False
            pass
        vagas = []
        # Como na pagina de pesquisa não aparece toda a descricao, tem que entrar em cada vaga para ler se exite.
        for j in teste:
            link = "https://br.indeed.com"+str(j['href'])
            # Verifica se a vaga já exite no banco
            mycursor = con.cursor()
            sql = "SELECT COUNT(*) AS cont FROM vagas WHERE `link` LIKE %s"
            mycursor.execute(sql, link)
            myresult = mycursor.fetchone()
            # Se não exite ele adicona
            if(myresult['cont'] == 0):
                print('Nova vaga: '+str(cont) +
                      ' - Data: ' + str(datetime.today())+" - " + str(s.proxies))
                titulo = j.find(
                    'h2', class_="jobTitle").findAll('span')[-1].text
                cidade = j.find('div', class_="companyLocation").text
                descricao = BeautifulSoup(s.get(link, timeout=10).text, 'html.parser').find(
                    'div', class_="jobsearch-jobDescriptionText").text
                vaga = (str(titulo), str(link), str(cidade), str(descricao))
                with con.cursor() as c:
                    sql = "INSERT INTO `vagas` (`id`, `titulo`, `link`, `cidade`, `descricao`) VALUES (NULL, %s, %s,%s, %s);"
                    c.execute(sql, vaga)
                con.commit()
                cont += 1
        # print(page/10)
        page += 10
    except Exception as e:
        #status = False
        print("Erro:"+str(s.proxies))

# print(criaJSON(vagas))
# with open('indeed.json', 'w', encoding='utf8') as json_file:
 #   json.dump(criaJSON(vagas), json_file, ensure_ascii=False)
