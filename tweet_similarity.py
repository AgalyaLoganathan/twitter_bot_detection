import re
from Levenshtein import ratio
from nltk.corpus import stopwords
from pymongo import MongoClient
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("english")

client = MongoClient()
db = client.twitter
bot_collection = db.bot_collection
file_io = open('bot_similar_tweets.txt', 'a')

bot_accounts = bot_collection.distinct('name')
for bot_account in bot_accounts:
    bot_tweets = []
    bot_tweets_info = bot_collection.find({'name': bot_account})
    filtered_tweets = []
    for tweet in bot_tweets_info:
        tweet = tweet['tweet']
        tweet_tokens = tweet.split(' ')
        filtered_tweet = ' '.join([word for word in tweet_tokens if word not in stopwords.words('english')])
        filtered_tweet = re.sub(r"(?:@|http?\:/)\S+", '', filtered_tweet)
        filtered_tweet = ''.join([stemmer.stem(t) for t in filtered_tweet])
        filtered_tweets.append(filtered_tweet)

    count_of_similar_tweets = 0
    for i in range(0, len(filtered_tweets) - 2, +1):
        for j in range(i + 1, len(filtered_tweets) - 1, +1):
            try:
                if ratio(filtered_tweets[i], filtered_tweets[j]) >= 0.80:
                    count_of_similar_tweets += 1
            except:
                continue

    file_io.write(bot_account + "," +str(count_of_similar_tweets))
    file_io.write('\n')

file_io.close()
