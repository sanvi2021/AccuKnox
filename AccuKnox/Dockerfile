# Dockerfile

FROM python:3.9.12

WORKDIR /AccuKnox

ADD . /AccuKnox

COPY ./requirements.txt /AccuKnox/requirements.txt
 
RUN pip install -r requirements.txt

COPY . /AccuKnox/

CMD [ "python", "manage.py", "runserver","0.0.0.0:8000" ]

