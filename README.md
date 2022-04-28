# REST API для системы комментариев блога

## Тестовое задание
Реализовать REST API для системы комментариев блога.
### Функциональные требования:
У системы должны быть методы API, которые обеспечивают:
 - добавление статьи (Можно чисто номинально, как сущность, к которой крепятся комментарии)
 - добавление комментария к статье
 - добавление коментария в ответ на другой комментарий (возможна любая вложенность)
 - получение всех комментариев к статье вплоть до 3 уровня вложенности
 - получение всех вложенных комментариев для комментария 3 уровня
 - по ответу API комментариев можно воссоздать древовидную структуру

## Стек технологий
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)


## Описание проекта
Проект разворачивается в 3-х контейнерах: backend-приложение, postgresql-база данных и nginx-сервер.
Реализована авторизация через auth токены, настроена админка.
Приготовлены фикстуры для заполнения БД тестовыми данными 
Логин и пароль superuser - admin / qwerty234.

## Запуск проекта через Docker
- Клонировать репозиторий и перейти в него в командной строке.
Создать и активировать виртуальное окружение:
```
git clone https://github.com/Seniacat/test_api
cd test_api/
```
- Cоздать и открыть файл .env с переменными окружения:
```
cd infra/
touch .env
```
Заполнить .env файл с переменными окружения по примеру (SECRET_KEY см. в файле settings.py). 
Необходимые для работы проекта переменные окружения можно найти в файле .env.example в текущей директории:
```
echo DB_ENGINE=django.db.backends.postgresql >> .env

echo DB_NAME=postgres >> .env

echo POSTGRES_PASSWORD=postgres >> .env

echo POSTGRES_USER=postgres  >> .env

echo DB_HOST=db  >> .env

echo DB_PORT=5432  >> .env

echo SECRET_KEY=************ >> .env
```
- Установить и запустить приложения в контейнерах:
```
docker-compose up --build
```
Запустить миграции, собрать статику:
```
docker-compose exec backend python manage.py migrate

docker-compose exec backend python manage.py collectstatic --no-input 
```
Загрузить в БД тестовые данные:
```
docker-compose exec backend python manage.py loaddata data.json
```

## Документация к проекту 
Документация доступна [здесь](http://127.0.0.1/swagger/) после установки приложения.


## Запуск проекта в dev-режиме

- Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/Seniacat/test_api.git
cd test_api/
```
- Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
source env/bin/activate (Mac OS, Linux) или source venv/Scripts/activate (Win10)
```
- Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
- Cоздать в директории infra/ файл .env с переменными окружения:
```
cd infra/
touch .env
```
Заполнить .env файл с переменными окружения по примеру (SECRET_KEY см. в файле settings.py). 
Необходимые для работы проекта переменные окружения можно найти в файле .env.example в текущей директории:
```
echo DB_ENGINE=django.db.backends.postgresql >> .env

echo DB_NAME=postgres >> .env

echo POSTGRES_PASSWORD=postgres >> .env

echo POSTGRES_USER=postgres  >> .env

echo DB_HOST=db  >> .env

echo DB_PORT=5432  >> .env

echo SECRET_KEY=************ >> .env
```
- Выполнить миграции:
```
python3 manage.py migrate
```
Запустить проект:
```
python3 manage.py runserver
```

Документацию можно найти по [адресу](http://127.0.0.1:8000/swagger/)
