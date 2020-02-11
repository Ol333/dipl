# dipl
 Automated system for supporting computational experiments

#установка необходимых пакетов
Python 3.7.3 pip install -r requirements.txt

#установка базы данных PostgreSQL
apt-get install postgresql
#переключаемся на системного пользователя postgres              
su - postgres                            
#запускаем консоль управления PostgreSQL
psql       
#создаем пользователя                              
create user dipl_user with password 'dipl';   
#создаем базу данных
create datavase dipl_db;                 
#(можно задать другие названия/пароль и изменить файл postgres_settings.txt)
#выход
exit
