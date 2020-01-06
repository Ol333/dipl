#!/usr/bin/python3
import psycopg2
from datetime import datetime

array=[]
with open('postgres_settings.txt', 'r') as f:
    array = [row.strip().split('"')[1] for row in f]

try: #подключаемся к бд
    connection = psycopg2.connect(dbname=array[0], user=array[1],
                    password=array[2], host=array[3])
    print("PostgreSQL connection is open " + datetime.now().isoformat(sep=' ')+'\n')
    cursor = connection.cursor()
except(Exception, psycopg2.Error) as error:
    print("Connection error "+str(error)+' ' + datetime.now().isoformat(sep=' ')+'\n')

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
connection.close()
