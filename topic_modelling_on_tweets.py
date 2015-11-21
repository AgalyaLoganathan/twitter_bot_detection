import re

import numpy as np
import nltk
from nltk.corpus import stopwords
from pymongo import MongoClient
from nltk.stem.snowball import SnowballStemmer
from gensim import corpora, models

cachedStopWords = set(stopwords.words("english"))

cachedStopWords.update(('and', 'I', 'a', 'and', 'so', 'arnt', 'this', 'when', 'tt',
                        'many', 'Many', 'so', 'cant', 'be', 'in', 'yes', 'No', 'no',
                        'These', 'these', 'not', 'maybe', 'never', 'how', 'the', 'is', 'it','rt', 'to', 'it\'s'))

client = MongoClient()
db = client.twitter
bot_collection = db.bot_collection
snowballStemmer = SnowballStemmer("english")



def tokenize_and_stem(text):
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


def get_topic_words(input_tweets):
    texts = [tokenize_and_stem(text) for text in input_tweets]
    dictionary = corpora.Dictionary(texts)
    dictionary.filter_extremes(no_below=1, no_above=0.8)
    corpus = [dictionary.doc2bow(text) for text in texts]
    lda = models.LdaModel(corpus, num_topics=3,
                          id2word=dictionary,
                          update_every=5,
                          chunksize=10000,
                          passes=100)

    lda.show_topics()
    topics_matrix = lda.show_topics(formatted=False, num_words=15)
    topics_matrix = np.array(topics_matrix)

    topic_words = topics_matrix[:, :, 1]
    processed_topic_words = []
    for topic in topic_words:
        words = []
        for word in topic:
            words.append(word.encode('utf-8'))
        processed_topic_words.append(words)
    return processed_topic_words


with open('data_collected/bot_similar_tweets.txt', 'r') as bot_file:
    for bot_info in bot_file:
        bot_info_array = bot_info.split(',')
        if bot_info_array[1] >= 200:
            try:
                bot_tweets_info = bot_collection.find({'name': bot_info_array[0]})
                filtered_tweets = []
                for tweet in bot_tweets_info:
                    tweet = tweet['tweet']
                    tweet_tokens = tweet.split(' ')
                    filtered_tweet = ' '.join([word for word in tweet_tokens if word not in cachedStopWords and len(word)> 2])
                    filtered_tweet = re.sub(r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', '',
                                            filtered_tweet)  # Remove URLS
                    filtered_tweet = re.sub(r'<[^>]+>', '', filtered_tweet)  # HTML tags
                    filtered_tweet = re.sub(r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", '', filtered_tweet)  # Hashtags
                    filtered_tweet = re.sub(r'(?:@[\w_]+)', '', filtered_tweet)  # @-mentions
                    filtered_tweet = re.sub('[^A-Za-z0-9\s]+', '', filtered_tweet)  # Remove every other special characters
                    filtered_tweet = re.sub('\s+', ' ', filtered_tweet).strip()  # Convert mutliple space to single space
                    # filtered_tweet = ''.join([stemmer.stem(t) for t in filtered_tweet])
                    filtered_tweets.append(''.join(str(filtered_tweet.lower())))
                file_output = open('bot_topic_modelling.txt', 'a')
                file_output.write(bot_info_array[0] + "," + str(get_topic_words(filtered_tweets)))
                file_output.write('\n')
                file_output.close()
            except:
                print("Error processing " + str(bot_info_array[0]))
                continue



