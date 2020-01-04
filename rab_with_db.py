#!/usr/bin/python3
import psycopg2
from datetime import datetime


array=[] #считываем параметры запуска и работы сервиса
with open('postgres_settings.txt', 'r') as f:
    array = [row.strip().split('"')[1] for row in f]

try: #подключаемся к бд
    connection = psycopg2.connect(dbname=array[0], user=array[1],
                    password=array[2], host=array[3])
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

def get_table_by_id(table_name,name_id,id):
    mas = []
    cursor.execute(f'SELECT * FROM "{table_name}" WHERE "{name_id}"={id};')
    for a in cursor.fetchall():
        mas.append(a)
    return mas

def get_value(param_id,res_id):
    cursor.execute(f'SELECT * FROM "value" WHERE "Parameter_id"={param_id} AND "Result_id"={res_id};')
    for a in cursor.fetchall():
        return a

def add_(proj,modules_ParamValueRes):
    cursor.execute("""INSERT INTO "project" ("Id","Name","Path")
                    VALUES (default,'{}','{}')
                    RETURNING "Id";
                    """.format(proj[0],proj[1]))
    id_proj = cursor.fetchall()[0][0]

    for mod in modules_ParamValueRes:
        cursor.execute("""INSERT INTO "module" ("Id","Name","Path","Project_id")
                        VALUES (default,'{}','{}',{})
                        RETURNING "Id";
                        """.format(mod[0],mod[1],id_proj))
        id_mod = cursor.fetchall()[0][0]
        # res

        cursor.execute("""INSERT INTO "result" ("Id","Path","File_extension" ,"Project_id","Date","Time")
                        VALUES (default,'{}','{}',{},'{}','{}')
                        RETURNING "Id";
                        """.format(mod[3].replace("'",'"'),"",id_proj,datetime.now().isoformat(sep=' '),datetime.now().isoformat(sep=' ')))
        id_res = cursor.fetchall()[0][0]
        for PV in mod[2]:
            param,value = PV.split('=')
            cursor.execute("""INSERT INTO "parameter" ("Id","Module_id","Name","Type_value")
                            VALUES (default,{},'{}','{}')
                            RETURNING "Id";
                            """.format(id_mod,param.strip(),"string"))
            id_param = cursor.fetchall()[0][0]
            cursor.execute("""INSERT INTO "value" ("Id","Parameter_id","Value","Result_id" )
                            VALUES (default,{},'{}',{});
                            """.format(id_param,value.strip().strip("'"),id_res))
    # cursor.execute()
    connection.commit()



# connection.close()
