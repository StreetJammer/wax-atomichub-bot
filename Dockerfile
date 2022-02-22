FROM joyzoursky/python-chromedriver:3.8

RUN apt-get update
RUN pip install --upgrade pip

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -r requirements.txt

COPY . .

RUN export PYTHONPATH=/app

