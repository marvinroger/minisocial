FROM python:2.7

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
RUN python manage.py migrate

VOLUME ["/code/db.sqlite3"]
EXPOSE 8000

RUN "python manage.py runserver"
