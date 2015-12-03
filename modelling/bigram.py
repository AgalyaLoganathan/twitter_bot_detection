import re
from Levenshtein import ratio
from nltk.corpus import stopwords
from pymongo import MongoClient
from nltk.stem.snowball import SnowballStemmer
import nltk
from nltk.tokenize import TweetTokenizer
import re

stemmer = SnowballStemmer("english")

client = MongoClient()
db = client.twitter

print "**********************************"
print "Entering Bot data"
print "**********************************"

bot_collection = db.bot_collection
file_io = open('BotbiGramCount.csv', 'a')
bot_accounts = bot_collection.distinct('name')
total_tweets = ''
filtered_tweets = ""
count = 0
for bot_account in bot_accounts:
    bot_tweets = []
    bot_tweets_info = bot_collection.find({'name': bot_account})


    for tweet in bot_tweets_info:
        tweet = tweet['tweet']
        total_tweets = total_tweets + ' ' + tweet

tweet_tokens = total_tweets.split(' ')
filtered_tweet = ' '.join([word for word in tweet_tokens if word not in stopwords.words('english')])
filtered_tweet = re.sub(r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', '', filtered_tweet) #Remove URLS
filtered_tweet = re.sub(r'<[^>]+>', '', filtered_tweet) # HTML tags
filtered_tweet = re.sub(r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",'', filtered_tweet) # Hashtags
filtered_tweet = re.sub(r'(?:@[\w_]+)','', filtered_tweet)  # @-mentions
filtered_tweet = re.sub('[^A-Za-z0-9\s]+', '', filtered_tweet) # Remove everyother special characters
filtered_tweet = re.sub( '\s+', ' ', filtered_tweet).strip() # Convert mutliple space to single space
filtered_tweet = ''.join([stemmer.stem(t) for t in filtered_tweet])
filtered_tweets = filtered_tweets + " " + filtered_tweet
#Create some text and tokenize it
tknzr = TweetTokenizer()
tokens = tknzr.tokenize(filtered_tweets)
#Initialize finder object with the tokens
finder = nltk.collocations.BigramCollocationFinder.from_words(tokens)
#Build a dictionary with bigrams and their frequencies
bigram_measures = nltk.collocations.BigramAssocMeasures()
scored = dict(finder.score_ngrams(bigram_measures.raw_freq))
results = dict(sorted(scored.items(), key=lambda x:x[1],reverse=True)[:10])
print(results)
file_io.write(str(results))
file_io.write('\n')
    # sum=0
    # for result in results.values():
    #    sum = sum+result
    # print sum
    # file_io.write(bot_account + "," + str(sum))
    # file_io.write('\n')
file_io.close()
