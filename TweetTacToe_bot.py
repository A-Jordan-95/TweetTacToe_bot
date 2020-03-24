import tweepy
import random
from time import sleep
from credentials import *
from bot_definitions import check_for_and_play_game

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

while True:
    check_for_and_play_game(api)
    sleep(2)
#end main game loop
