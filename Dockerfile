FROM python:3.8-slim-buster

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update

RUN apt-get -y install gcc

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

VOLUME ["/app"]

EXPOSE 8080

CMD ["python", "api/main.py"]