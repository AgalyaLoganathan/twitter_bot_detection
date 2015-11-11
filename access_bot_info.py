from pymongo import MongoClient

client = MongoClient()
db = client.twitter
bot_collection = db.bot_collection
file_io = open('friends_ratio.csv', 'a')

bot_accounts = bot_collection.distinct('name')
for bot_account in bot_accounts:
    bot = bot_collection.find_one({'name': bot_account})
    followers_count = bot['followers_count']
    friends_count = bot['friends_count']
    if followers_count != 0 and friends_count != 0:
        friends_ratio = float(friends_count) / float(friends_count * followers_count)
    else:
        friends_ratio = 0
    print("User " + bot_account + " has ratio: " + str(friends_ratio))

    file_io.write(bot_account + ", " + str(friends_ratio))
    file_io.write('\n')

file_io.close()
