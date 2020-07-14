FROM parasjain1996/sparkbase
ENV PYTHONUNBUFFERED 1
RUN curl https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.11/2.4.6/spark-sql-kafka-0-10_2.11-2.4.6.jar -o /opt/bitnami/spark/jars/org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.6.jar
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
COPY ./mtwitter /opt/bitnami/python/lib/python3.6/site-packages/mtwitter
COPY ./nltk_data /home/spark/nltk_data