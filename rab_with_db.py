#!/usr/bin/python3
import psycopg2
from datetime import datetime


try: #подключаемся к бд
    connection = psycopg2.connect(dbname='dipl_db', user='dipl_user',
                    password='dipl', host='localhost')
    print("PostgreSQL connection is open " + datetime.now().isoformat(sep=' ')+'\n')
    cursor = connection.cursor()
except(Exception, psycopg2.Error) as error:
    print("Connection error "+str(error)+' ' + datetime.now().isoformat(sep=' ')+'\n')



def get_table(table_name):
    mas = []
    cursor.execute(f'SELECT * FROM "{table_name}";')
    for a in cursor.fetchall():
        mas.append(a)
    return mas



# #авторизация
# cursor.execute(("""SELECT id,password,system FROM "authorization" WHERE login='{}';""").format(login))
# id_author, pas, syst = cursor.fetchall()[0]
# if (password == pas):
# #проверяем полномочия
# cursor.execute(("""SELECT id_action FROM "powers" WHERE id_autorization='{}';""").format(id_author))
# id_act = cursor.fetchall()[0][0]
# cursor.execute(("""SELECT name FROM "action_list" WHERE id='{}';""").format(id_act))


# connection.close()
