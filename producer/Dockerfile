FROM python:3.6-slim-buster
ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir pyspark==2.4.5
RUN mkdir /usr/share/man/man1/
RUN apt-get -y update && \
    apt-get install -y software-properties-common && \
    apt-add-repository 'deb http://security.debian.org/debian-security stretch/updates main' && \
    apt-get -y update && \
    apt-get install -y openjdk-8-jdk
RUN pip install --no-cache-dir pykafka==2.8
RUN pip install --no-cache-dir python-twitter==3.5


RUN mkdir /app
WORKDIR /app

COPY ./ /app

CMD ["python /app/kafka_producer.py"]