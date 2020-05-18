import tweepy
import random
from time import sleep
from credentials import *
from bot_definitions import *

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
the_bot = bot()

while True:
    the_bot.check_for_and_play_game(api)
    sleep(3)
#end main game loop
