'''
                Script by Faisal K
                    http://faisal-k.com
                    http://twitter.com/kwmx
                    GitHub repository:
                This script is just an example of how to use tweepy along with DataManager to make a twitter bot in python
                Please note that the retweet code has been commented out because of twitter policy against bulk retweeting. Keep it in mind and please respect twitter's polices
'''
#Import libraries
from time import sleep
from DataManager import BotSql
import tweepy


#The info about the twitter app (https://apps.twitter.com)
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
#Connection
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth.secure = True

api = tweepy.API(auth)

#  Define myBot as a twitter user which refrence the user running the scrript. Define botsql for the database
myBot = api.me()
#devList = api.get_list('@' + myBot.screen_name, slug='list-name')  #If you have a list you can use this line
botsql = BotSql()


#Show information
print("Connected as: @" + myBot.screen_name + "\n Current database stats: \n" + botsql.get_stats())

#start going thorugh the hashtag specified
for tweet in tweepy.Cursor(api.search, q="#bottest").items():
    errcount = 0
    tweetid = 0
    try:
        #If one of these conditions (The tweet is stored in the database or the user is banned
        if (tweet.user.id == myBot.id) or (botsql.check_Ban(str(tweet.user.id))) or (botsql.check_Tweet(str(tweet.id))):
            continue
        tweetid = str(tweet.id)
        botsql.add_Tweet(tweetid, str(tweet.user.id))
        print("\nUsername: @" + tweet.user.screen_name)
        if (tweet.retweeted == False):
            #tweet.retweet()
            print("Retweeted the tweet: \n(( " + tweet.text + " ))")

        errcount = 0
    except tweepy.TweepError as e:
        print(e)
        botsql.remove_Tweet(tweetid)
        ++errcount
        if(errcount > 10):
            print("Pausing for 30 minutes")
            sleep(1800)
        else:
            errcount = 0
            sleep(10)
        continue

print("Finished run. New database stats:\n " + botsql.get_stats())
