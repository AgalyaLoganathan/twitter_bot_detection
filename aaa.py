file_io = open("data_collected/bot_daily_tweet_frequency.csv", "a")
user_accounts = user_collection.distinct('name')
for user_account in user_accounts:
    user_tweet_times = []
    bot_tweets = user_collection.find({'name': user_account})
    for tweet in bot_tweets:
        tweet_creation_time = tweet['created_at']
        user_tweet_times.append(parser.parse(tweet_creation_time))

    tweet_trend = []
    user_tweet_times.sort()
    tweets_grouped_by_date = [(dt, len(list(grp))) for dt, grp in
                              itertools.groupby(user_tweet_times, key=lambda x: x.date())]
    for date in tweets_grouped_by_date:
        tweet_trend.append(date[1])
    mean_value = mean(tweet_trend)
    standard_error = calculate_standard_error(tweet_trend, mean_value)

    count_of_days = 0.0
    for entry in tweet_trend:
        if entry < (mean_value - standard_error) or entry > (mean_value + standard_error):
            count_of_days += 1

    trend = (count_of_days / len(tweet_trend))*100
    file_io.write(user_account + " , " + str(trend))
    file_io.write('\n')

file_io.close()