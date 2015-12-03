from itertools import groupby
import itertools
from numpy import require
from dateutil import parser
from pymongo import MongoClient
import time
import re

client = MongoClient()
db = client.twitter
bot_collection = db.bot_collection
file_io = open('data_collected/bot_rt_count.txt', 'a')

bot_accounts = bot_collection.distinct('name')
for bot_account in bot_accounts:
    bot_tweet_times = []
    bot_tweets = bot_collection.find({'name': bot_account})
    count_of_retweeted_tweets = 0.0
    total_tweets = 0
    for tweet in bot_tweets:
        total_tweets += 1
        flag = re.match(r'RT\s@...+',tweet['tweet'])
        if flag:
            count_of_retweeted_tweets += 1.0

    mentions_feature = count_of_retweeted_tweets / total_tweets
    file_io.write(bot_account+","+str(mentions_feature))
    file_io.write('\n')

file_io.close()
