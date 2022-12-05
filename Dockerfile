
FROM python:3.7 AS builder

RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

ENV FLASK_APP  src
WORKDIR /project
ADD . /project 

ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0"]