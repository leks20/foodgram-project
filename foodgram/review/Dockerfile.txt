FROM python:3.8

RUN pip install --upgrade pip

WORKDIR /home/app/web
RUN mkdir /home/app/web/static
RUN mkdir /home/app/web/media

COPY . /home/app/web

RUN pip install -r /home/app/web/requirements.txt

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
