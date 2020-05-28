#!/usr/bin/python3
import psycopg2
from datetime import datetime

class DbWork():
    def __init__(self):
        array=[] #считываем параметры
        with open('postgres_settings.txt', 'r') as f:
            array = [row.strip().split('"')[1] for row in f]
        try: #подключаемся к бд
            self.connection = psycopg2.connect(dbname=array[0], user=array[1],
                            password=array[2], host=array[3])
            print("PostgreSQL self.connection is open " + datetime.now().isoformat(sep=' ')+'\n')
            self.cursor = self.connection.cursor()

            self.cursor.execute('SELECT "table_name" FROM information_schema.tables;')
            set_of_tables = set()
            for a in self.cursor.fetchall():
                set_of_tables.add(a[0])
            if not set(["project","module","parameter","result","value","binding"]).issubset(set_of_tables):
                print(set_of_tables)
                self.create_db_tables()
        except(Exception, psycopg2.Error) as error:
            print("self.connection error "+str(error)+' ' + datetime.now().isoformat(sep=' ')+'\n')



    def create_db_tables(self):
        self.cursor.execute("""CREATE TABLE "project" ("Id" serial NOT NULL,
                                                	"Name" VARCHAR(255) NOT NULL,
                                                	"Path" VARCHAR(255) NOT NULL,
                                                	CONSTRAINT "project_pk" PRIMARY KEY ("Id")
                                                    ) WITH (OIDS=FALSE);
                        """)

        self.cursor.execute("""CREATE TABLE "module" ("Id" serial NOT NULL,
                                                    "Name" VARCHAR(255) NOT NULL,
                                                    "Path" VARCHAR(255) NOT NULL,
                                                    CONSTRAINT "module_pk" PRIMARY KEY ("Id")
                                                    ) WITH (OIDS=FALSE);
                        """)

        self.cursor.execute("""CREATE TABLE "parameter" ("Id" serial NOT NULL,
                                                        "Module_id" integer NOT NULL,
                                                        "Name" VARCHAR(255) NOT NULL,
                                                        "Type_value" VARCHAR(255) NOT NULL,
                                                        CONSTRAINT "parameter_pk" PRIMARY KEY ("Id")
                                                    ) WITH (OIDS=FALSE);
                        """)

        self.cursor.execute("""CREATE TABLE "value" ("Id" serial NOT NULL,
                                                    "Parameter_id" integer NOT NULL,
                                                    "Value" VARCHAR(255) NOT NULL,
                                                    "Binding_id" integer NOT NULL,
                                                    CONSTRAINT "value_pk" PRIMARY KEY ("Id")
                                                    ) WITH (OIDS=FALSE);
                        """)

        self.cursor.execute("""CREATE TABLE "result" ("Id" serial NOT NULL,
                                                    "Path" VARCHAR(255) NOT NULL,
                                                    "File_extension" VARCHAR(255) NOT NULL,
                                                    "Project_id" integer NOT NULL,
                                                    "Date" DATE NOT NULL,
                                                    "Time" TIME NOT NULL,
                                                    CONSTRAINT "result_pk" PRIMARY KEY ("Id")
                                                    ) WITH (OIDS=FALSE);
                        """)

        self.cursor.execute("""CREATE TABLE "binding" ("Id" serial NOT NULL,
                                                    "Order_number" integer NOT NULL,
                                                	"Count" integer NOT NULL,
                                                	"Project_id" integer NOT NULL,
                                                	"Module_id" integer NOT NULL,
                                                    CONSTRAINT "binding_pk" PRIMARY KEY ("Id")
                                                    ) WITH (OIDS=FALSE);
                        """)

        self.cursor.execute("""ALTER TABLE "parameter"
                            ADD CONSTRAINT "parameter_fk0"
                            FOREIGN KEY ("Module_id")
                            REFERENCES "module"("Id");""")

        self.cursor.execute("""ALTER TABLE "value"
                            ADD CONSTRAINT "value_fk0"
                            FOREIGN KEY ("Parameter_id")
                            REFERENCES "parameter"("Id");""")

        self.cursor.execute("""ALTER TABLE "value"
                            ADD CONSTRAINT "value_fk1"
                            FOREIGN KEY ("Binding_id")
                            REFERENCES "binding"("Id");""")

        self.cursor.execute("""ALTER TABLE "result"
                            ADD CONSTRAINT "result_fk0"
                            FOREIGN KEY ("Project_id")
                            REFERENCES "project"("Id");""")

        self.cursor.execute("""ALTER TABLE "binding"
                            ADD CONSTRAINT "binding_fk0"
                            FOREIGN KEY ("Project_id")
                            REFERENCES "project"("Id");""")

        self.cursor.execute("""ALTER TABLE "binding"
                            ADD CONSTRAINT "binding_fk1"
                            FOREIGN KEY ("Module_id")
                            REFERENCES "module"("Id");""")

        self.connection.commit()

    def get_table(self,table_name):
        mas = []
        self.cursor.execute(f'SELECT * FROM "{table_name}";')
        for a in self.cursor.fetchall():
            mas.append(a)
        return mas

    def get_table_by_id(self,table_name,name_id,id):
        mas = []
        self.cursor.execute(f'SELECT * FROM "{table_name}" WHERE "{name_id}"={id};')
        for a in self.cursor.fetchall():
            mas.append(a)
        return mas

    def get_value(self,param_id,res_id):
        self.cursor.execute(f'SELECT * FROM "value" WHERE "Parameter_id"={param_id} AND "Result_id"={res_id};')
        for a in self.cursor.fetchall():
            return a

    def select_proj(self,name,path):
        self.cursor.execute("""SELECT "Id"
                        FROM "project"
                        WHERE "Name"='{}' and "Path"='{}';
                        """.format(name,path))
        for a in self.cursor.fetchall():
            return a[0]

    def insert_proj(self,name,path):
        self.cursor.execute("""INSERT INTO "project" ("Id","Name","Path")
                        VALUES (default,'{}','{}')
                        RETURNING "Id";
                        """.format(name,path))
        return self.cursor.fetchall()[0][0]

    def select_module(self,name,path):
        mas = []
        self.cursor.execute("""SELECT "Id"
                        FROM "module"
                        WHERE "Name"='{}' and "Path"='{}';
                        """.format(name,path))
        for a in self.cursor.fetchall():
            mas.append(a[0])
        return mas

    def insert_module(self,name,path):
        self.cursor.execute("""INSERT INTO "module" ("Id","Name","Path")
                        VALUES (default,'{}','{}')
                        RETURNING "Id";
                        """.format(name,path))
        return self.cursor.fetchall()[0][0]

    def insert_res(self,path,file_ext,id_proj):
        self.cursor.execute("""INSERT INTO "result" ("Id","Path","File_extension" ,"Project_id","Date","Time")
                        VALUES (default,'{}','{}',{},'{}','{}')
                        RETURNING "Id";
                        """.format(path,file_ext,id_proj,datetime.now().isoformat(sep=' '),datetime.now().replace(microsecond=0).isoformat(sep=' ')))
        # self.connection.commit()
        return self.cursor.fetchall()[0][0]


    def insert_param(self,id_mod,param,type):
        self.cursor.execute("""INSERT INTO "parameter" ("Id","Module_id","Name","Type_value")
                        VALUES (default,{},'{}','{}')
                        RETURNING "Id";
                        """.format(id_mod,param,type))
        return self.cursor.fetchall()[0][0]

    def select_param(self,id_mod,param,type):
        self.cursor.execute("""SELECT "Id"
                        FROM "parameter"
                        WHERE "Module_id"={} and "Name"='{}' and "Type_value"='{}';
                        """.format(id_mod,param,type))
        for a in self.cursor.fetchall():
            return a[0]

    def insert_value(self,id_param,value,id_bind):
        self.cursor.execute("""INSERT INTO "value" ("Id","Parameter_id","Value","Binding_id" )
                        VALUES (default,{},'{}',{})
                        RETURNING "Id";
                        """.format(id_param,value,id_bind))
        return self.cursor.fetchall()[0][0]

    def insert_few_value(self,mas):
        s = """INSERT INTO "value" ("Id","Parameter_id","Value","Binding_id" )
               VALUES """
        for m in mas:
            s += """(default,{},'{}',{}), """.format(m[0],m[1],m[2])
        self.cursor.execute(s[:-2]+";")

    def select_binding(self,id_proj):
        mas = []
        self.cursor.execute("""SELECT "Id", "Module_id"
                        FROM "binding"
                        WHERE "Project_id"={};
                        """.format(id_proj))
        for a in self.cursor.fetchall():
            mas.append(a)
        return mas

    def insert_binding(self,numb,count,id_proj,id_mod):
        self.cursor.execute("""INSERT INTO "binding" ("Id","Order_number","Count","Project_id","Module_id" )
                        VALUES (default,{},{},{},{})
                        RETURNING "Id";
                        """.format(numb,count,id_proj,id_mod))
        return self.cursor.fetchall()[0][0]

    def delete_db_tables(self):
        self.cursor.execute("""
                        drop table project cascade;
                        drop table module cascade;
                        drop table parameter cascade;
                        drop table result cascade;
                        drop table value cascade;
                        drop table binding cascade;
                        """)
        self.connection.commit()

    # self.connection.close()
