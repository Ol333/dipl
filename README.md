# dipl
## Automated system for supporting computational experiments

***

#### Установка базы данных PostgreSQL.

> apt-get install postgresql

1. Переключение на системного пользователя postgres.             

> su - postgres                            

2. Запуск консоли управления PostgreSQL.

> psql       

3. Создание пользователя.

> create user dipl_user with password 'dipl';   

4. Создание базы данных.

> create database dipl_db;                 

(можно задать другие названия/пароль и изменить файл postgres_settings.txt)

5. Выход.

>exit

#### Установка необходимых пакетов.

> pip install pipenv
>
> pipenv shell
>
> pipenv install --ignore-pipfile
