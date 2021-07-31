import pymysql
con = pymysql.connect(host='127.0.0.1', user='root',
                      database='vagas', cursorclass=pymysql.cursors.DictCursor)
with con:
    with con.cursor() as c:
        sql = "INSERT INTO `vagas` (`id`, `titulo`, `link`, `cidade`, `descricao`) VALUES (NULL, %s, %s,%s, %s);"
        c.execute(sql, ('Titulo', 'https://google.com', 'Aracruz', 'Teste12'))

    con.commit()
    
    with con.cursor() as c:
        sql = "SELECT * FROM `vagas`"
        c.execute(sql)
        res = c.fetchall()
        for linha in res:
            print(linha['titulo'])

con.close()
