FROM python:3.6-slim-buster

ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir pyspark==2.4.5
RUN mkdir /usr/share/man/man1/
RUN apt-get -y update && \
    apt-get install -y software-properties-common && \
    apt-add-repository 'deb http://security.debian.org/debian-security stretch/updates main' && \
    apt-get -y update && \
    apt-get install -y openjdk-8-jdk

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./mtwitter /usr/local/lib/python3.6/site-packages/mtwitter

RUN mkdir /app
WORKDIR /app

COPY ./spark_consumer.py /app/spark_consumer.py

EXPOSE 54672
EXPOSE 4040
EXPOSE 4041

CMD ["python /app/spark_consumer.py"]