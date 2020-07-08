from nltk import word_tokenize, download
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
import re
import os
import numpy as np
from keras.models import model_from_json

from mtwitter.settings import BASE_DIR, num_features
from mtwitter.constants import abbreviations, similarities


class LemmaTokenizer:
    def __init__(self):
        self.wnl = WordNetLemmatizer()

    def __call__(self, doc):
        tokens = word_tokenize(doc)
        lemmatized_tokens = []
        for t in tokens:
            t = self.wnl.lemmatize(t)
            try:
                if t in abbreviations:
                    t = abbreviations[t]
                if t in similarities:
                    t = similarities[t]
                lemmatized_tokens.append(t)
            except LookupError:
                pass
        return lemmatized_tokens


def clean(text):
    special_char_regex = re.compile("[^A-Za-z0-9 ]+")
    mentions_regex = re.compile("^(?!.*?RT\s).+\s@\w+")
    highways_regex = re.compile("us[0-9]+")
    text = re.sub(special_char_regex, "", re.sub(mentions_regex, "", re.sub(highways_regex, "highway", text.lower())))
#     text = " ".join([p.text if not p.ent_type_ else p.ent_type_ for p in nlp(text)])
    return text.lower()


def encode_tweets(tweets, freq1_words):
    """
        function to encode tweets dataset into feature matrix
    """
    encoded_arr = np.zeros((len(tweets), num_features))
    for i in range(0, len(tweets)):
        tweet = tweets[i]     # for each tweet
        for j in range(0, num_features):    # for each feature
            tokens = freq1_words[j].split(" ")
            token = tokens[0]
            encoded_arr[i, j] = 0
            if token in set(tweet):
                encoded_arr[i, j] = 1
    return encoded_arr


def load_model(model_file_path):
    """
        Function to load the model from disk. Returns the model object.
    """
    model_dir = os.path.join(BASE_DIR, "model")
    # load json and create model
    json_file = open(os.path.join(model_dir, model_file_path + ".json"), 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(os.path.join(model_dir, model_file_path + ".h5"))
    print("Loaded model from disk")
    return loaded_model


vectorizer = CountVectorizer(
    min_df=1,
    stop_words='english',
    ngram_range=(1, 1),
    analyzer=u'word',
    tokenizer=LemmaTokenizer()
)

analyze = vectorizer.build_analyzer()