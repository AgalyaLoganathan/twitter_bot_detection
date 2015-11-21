from itertools import groupby
import itertools
import math
from numpy import mean
from dateutil import parser
from pymongo import MongoClient
import time

client = MongoClient()
db = client.twitter
bot_collection = db.bot_collection
file_io = open("data_collected/bot_daily_tweet_frequency.csv", "a")


def calculate_standard_error(values, mean_value):
   try:
    sum_of_diff = 0
    for i in values:
        sum_of_diff += (i - mean_value) * (i - mean_value)

    return math.sqrt(sum_of_diff / (len(values) - 1))
   except:
       print(values)
       raise


bot_accounts = bot_collection.distinct('name')
for bot_account in bot_accounts:
    bot_tweet_times = []
    bot_tweets = bot_collection.find({'name': bot_account})
    for tweet in bot_tweets:
        tweet_creation_time = tweet['created_at']
        bot_tweet_times.append(parser.parse(tweet_creation_time))

    tweet_trend = []
    bot_tweet_times.sort()
    tweets_grouped_by_date = [(dt, len(list(grp))) for dt, grp in
                              itertools.groupby(bot_tweet_times, key=lambda x: x.date())]
    for date in tweets_grouped_by_date:
        tweet_trend.append(date[1])
    mean_value = mean(tweet_trend)
    standard_error = calculate_standard_error(tweet_trend, mean_value)

    count_of_days = 0.0
    for entry in tweet_trend:
        if entry < (mean_value - standard_error) or entry > (mean_value + standard_error):
            count_of_days += 1

    trend = count_of_days / len(tweet_trend)
    file_io.write(bot_account + " , " + str(trend))
    file_io.write('\n')

file_io.close()
