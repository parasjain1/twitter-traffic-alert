from mtwitter.constants import traffic_keywords
from mtwitter.preprocess import load_model, encode_tweets, analyze, clean
from mtwitter.settings import model_file_path

model = load_model(model_file_path)


def predict(tweets):
    _tweets = []
    for tweet in tweets:
        tweet = clean(tweet)
        tokenized = analyze(tweet)
        _tweets.append(tokenized)
        # print(tokenized)
    encoded = encode_tweets(_tweets, traffic_keywords)
    return model.predict_classes(encoded, verbose=0)
