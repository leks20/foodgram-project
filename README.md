# FOODGRAM

Онлайн-сервис, где пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд

Cоздан в качестве дипломного проекта учебного курса Яндекс.Практикум.

[FOODGRAM](http://food-gram.tk) - пример работы сайта


## Стек технологий
- проект написан на Python с использованием веб-фреймворка Django.
- работа с изображениями - sorl-thumbnail, pillow
- развернут на сервере Яндекс.Облако - nginx, ginicorn
- база данны PostgreSQL
- автоматическое развертывание проекта - Docker, docker-compose
- система управления версиями - git

## Как запустить проект, используя Docker:
1) Клонируйте репозитроий с проектом:
```
git clone https://github.com/leks20/foodgram-project
```
2) В директории проекта создайте файл .env, в котором пропишите следующие переменные окружения (для тестирования можете использовать указанные значения переменных):
SECRET_KEY = '^k29dzdk)$y3brl78zg&hc2kcfxla(mr5et&(a64b)!(73fc1l'
SQL_DATABASE=foodgram_db
SQL_USER=leks20
SQL_PASSWORD=foodgram
SQL_HOST=db
SQL_PORT=5432
POSTGRES_USER=leks20
POSTGRES_PASSWORD=foodgram
POSTGRES_DB=foodgram_db
3) С помощью Dockerfile и docker-compose.yaml разверните проект:
```
docker-compose up --build
```
4) В новом окне терминала узнайте id контейнера foodgram_web и войдите в контейнер:
```
docker container ls
```
```
docker exec -it <CONTAINER_ID> bash
```
5) В контейнере выполните миграции, создайте суперпользователя:
```
python manage.py migrate

python manage.py createsuperuser
```
