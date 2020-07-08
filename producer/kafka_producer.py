import twitter
from pykafka import KafkaClient


from settings import *
from constants import locations, traffic_keywords

api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN,
                  access_token_secret=ACCESS_SECRET)

stream = api.GetStreamFilter(
    track=traffic_keywords,
    locations=locations,
    languages=['en']
)


bootstrap_servers = 'kafka:9092'    # change if your brokers live else where
client = KafkaClient(hosts=bootstrap_servers)
topic = client.topics["twitter-test"]
producer = topic.get_producer(use_rdkafka=False, max_request_size=262144000)

# producer.stop()  # Will flush background queue


def on_receive_tweet(tweet):
    tweet = tweet + "\n"
    producer.produce(bytes(tweet, 'utf-8'))


def start_streaming():
    while True:
        for tweet in stream:
            if tweet.get('text') is None:
                continue
            on_receive_tweet(tweet.get('text'))
        break


if __name__ == '__main__':
    start_streaming()
