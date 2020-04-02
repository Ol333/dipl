#!/usr/bin/python3
import psycopg2
from datetime import datetime

def create_db_tables():
    cursor.execute("""CREATE TABLE "project" ("Id" serial NOT NULL,
                                            	"Name" VARCHAR(255) NOT NULL,
                                            	"Path" VARCHAR(255) NOT NULL,
                                            	CONSTRAINT "project_pk" PRIMARY KEY ("Id")
                                                ) WITH (OIDS=FALSE);
                    """)

    cursor.execute("""CREATE TABLE "module" ("Id" serial NOT NULL,
                                                "Name" VARCHAR(255) NOT NULL,
                                                "Path" VARCHAR(255) NOT NULL,
                                                "Project_id" integer NOT NULL,
                                                CONSTRAINT "module_pk" PRIMARY KEY ("Id")
                                                ) WITH (OIDS=FALSE);
                    """)

    cursor.execute("""CREATE TABLE "parameter" ("Id" serial NOT NULL,
                                                    "Module_id" integer NOT NULL,
                                                    "Name" VARCHAR(255) NOT NULL,
                                                    "Type_value" VARCHAR(255) NOT NULL,
                                                    CONSTRAINT "parameter_pk" PRIMARY KEY ("Id")
                                                ) WITH (OIDS=FALSE);
                    """)

    cursor.execute("""CREATE TABLE "value" ("Id" serial NOT NULL,
                                                "Parameter_id" integer NOT NULL,
                                                "Value" VARCHAR(255) NOT NULL,
                                                "Result_id" integer NOT NULL,
                                                CONSTRAINT "value_pk" PRIMARY KEY ("Id")
                                                ) WITH (OIDS=FALSE);
                    """)

    cursor.execute("""CREATE TABLE "result" ("Id" serial NOT NULL,
                                                "Path" VARCHAR(255) NOT NULL,
                                                "File_extension" VARCHAR(255) NOT NULL,
                                                "Project_id" integer NOT NULL,
                                                "Date" DATE NOT NULL,
                                                "Time" TIME NOT NULL,
                                                CONSTRAINT "result_pk" PRIMARY KEY ("Id")
                                                ) WITH (OIDS=FALSE);
                    """)

    cursor.execute("""ALTER TABLE "module"
                        ADD CONSTRAINT "module_fk0"
                        FOREIGN KEY ("Project_id")
                        REFERENCES "project"("Id");""")

    cursor.execute("""ALTER TABLE "parameter"
                        ADD CONSTRAINT "parameter_fk0"
                        FOREIGN KEY ("Module_id")
                        REFERENCES "module"("Id");""")

    cursor.execute("""ALTER TABLE "value"
                        ADD CONSTRAINT "value_fk0"
                        FOREIGN KEY ("Parameter_id")
                        REFERENCES "parameter"("Id");""")

    cursor.execute("""ALTER TABLE "value"
                        ADD CONSTRAINT "value_fk1"
                        FOREIGN KEY ("Result_id")
                        REFERENCES "result"("Id");""")

    cursor.execute("""ALTER TABLE "result"
                        ADD CONSTRAINT "result_fk0"
                        FOREIGN KEY ("Project_id")
                        REFERENCES "project"("Id");""")

    connection.commit()


array=[] #считываем параметры
with open('postgres_settings.txt', 'r') as f:
    array = [row.strip().split('"')[1] for row in f]
try: #подключаемся к бд
    connection = psycopg2.connect(dbname=array[0], user=array[1],
                    password=array[2], host=array[3])
    print("PostgreSQL connection is open " + datetime.now().isoformat(sep=' ')+'\n')
    cursor = connection.cursor()

    cursor.execute('SELECT "table_name" FROM information_schema.tables;')
    set_of_tables = set()
    for a in cursor.fetchall():
        set_of_tables.add(a[0])
    if not set(["project","module","parameter","result","value"]).issubset(set_of_tables):
        print(set_of_tables)
        create_db_tables()
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

        for j in range(3,len(mod)):
            # res
            cursor.execute("""INSERT INTO "result" ("Id","Path","File_extension" ,"Project_id","Date","Time")
                            VALUES (default,'{}','{}',{},'{}','{}')
                            RETURNING "Id";
                            """.format(mod[j].replace("'",'"'),"",id_proj,datetime.now().isoformat(sep=' '),datetime.now().replace(microsecond=0).isoformat(sep=' ')))
            id_res = cursor.fetchall()[0][0]
            for PV in mod[2]:
                param,value = PV.split('=',1)
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


def delete_db_tables():
    cursor.execute("""
                    drop table project cascade;
                    drop table module cascade;
                    drop table parameter cascade;
                    drop table result cascade;
                    drop table value cascade;
                    """)
    connection.commit()


# connection.close()
