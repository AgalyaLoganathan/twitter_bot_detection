from itertools import groupby
import itertools
from numpy import require
from dateutil import parser
from pymongo import MongoClient
import time

client = MongoClient()
db = client.twitter
bot_collection = db.bot_collection
file_io = open('bot_avg_tweets_per_day.txt', 'a')

bot_accounts = bot_collection.distinct('name')
for bot_account in bot_accounts:
    # file_io.write("Bot name:  ")
    # file_io.write(bot_account)
    # file_io.write('\n')
    bot_tweet_times = []
    bot_tweets = bot_collection.find({'name': bot_account})
    for tweet in bot_tweets:
        tweet_creation_time = tweet['created_at']
        bot_tweet_times.append(parser.parse(tweet_creation_time))

    count_of_tweets = 0
    bot_tweet_times.sort()
    tweets_grouped_by_date = [(dt, len(list(grp))) for dt, grp in itertools.groupby(bot_tweet_times, key=lambda x: x.date())]
    for date in tweets_grouped_by_date:
        count_of_tweets += date[1]
    avg_tweets_per_day = count_of_tweets/len(tweets_grouped_by_date)
    file_io.write(str(bot_account) + " " + str(avg_tweets_per_day))
    file_io.write('\n')

file_io.close()



user_collection = db.user_collection
file_io = open('user_avg_tweets_per_day.txt', 'a')

user_accounts = user_collection.distinct('name')
for user_account in user_accounts:
    # file_io.write("Bot name:  ")
    # file_io.write(user_account)
    # file_io.write('\n')
    tweet_times = []
    tweets = user_collection.find({'name': user_account})
    for tweet in tweets:
        tweet_creation_time = tweet['created_at']
        tweet_times.append(parser.parse(tweet_creation_time))

    count_of_tweets = 0
    tweet_times.sort()
    tweets_grouped_by_date = [(dt, len(list(grp))) for dt, grp in itertools.groupby(tweet_times, key=lambda x: x.date())]
    for date in tweets_grouped_by_date:
        count_of_tweets += date[1]
    avg_tweets_per_day = count_of_tweets/len(tweets_grouped_by_date)
    file_io.write(str(user_account) + " " + str(avg_tweets_per_day))
    file_io.write('\n')

file_io.close()
