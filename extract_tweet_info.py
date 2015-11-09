import glob
import ast
import json
from pymongo import MongoClient

client = MongoClient()
db = client.twitter
bot_collection = db.bot_collection
user_collection = db.user_collection

bots_files_location = "/Users/agalya/Downloads/i_bot_detection/bots/*json" # replace the location with your file location

bot_files = glob.glob(bots_files_location)
for json_file in bot_files:
    json_contents = open(json_file).read()
    if json_contents == '401' or json_contents == 'deleted':
        continue
    else:

        try:
            bot_json = ast.literal_eval(json_contents)
            for bot in bot_json:
                bot_collection.insert({
                    'name': bot['user']['screen_name'],
                    'tweet': bot['text'],
                    'description': bot['user']['description'],
                    'location_coordinates': bot['coordinates'],
                    'created_at' : bot['created_at'],
                    'likes': bot['favorite_count'],
                    'retweet_count': bot['retweet_count'],
                    'is_retweeted': bot['retweeted'],
                    'source': bot['source'],
                    'user_details': bot['user'],
                    'mentions': bot['entities']['user_mentions'],
                    'hashtags': bot['entities']['hashtags'],
                    'urls': bot['entities']['urls'],
                    'followers_count': bot['user']['followers_count'],
                    'friends_count': bot['user']['friends_count'],
                    'user_profile_location': bot['user']['location'],
                    'time_zone': bot['user']['time_zone']
                })
        except:
            print("Error parsing bot file")
            print(json_file)


print("Finished bots ")

humans_files_location = "/Users/agalya/Downloads/i_bot_detection/humans/*json" # replace the location with your file location

human_files = glob.glob(humans_files_location)
for json_file in human_files:
    json_contents = open(json_file).read()
    if json_contents == '401' or json_contents == 'deleted':
        continue
    else:

        try:
            user_json = json.loads(json_contents)
            for user in user_json:
                user_collection.insert({
                    'name': user['user']['screen_name'],
                    'tweet': user['text'],
                    'description': user['user']['description'],
                    'location_coordinates': user['coordinates'],
                    'created_at' : user['created_at'],
                    'likes': user['favorite_count'],
                    'retweet_count': user['retweet_count'],
                    'is_retweeted': user['retweeted'],
                    'source': user['source'],
                    'user_details': user['user'],
                    'mentions': user['entities']['user_mentions'],
                    'hashtags': user['entities']['hashtags'],
                    'urls': user['entities']['urls'],
                    'followers_count': user['user']['followers_count'],
                    'friends_count': user['user']['friends_count'],
                    'user_profile_location': user['user']['location'],
                    'time_zone': user['user']['time_zone']
                })

        except:
            print("Error parsing user file")
            print(json_file)

print("Finished Humans ")
