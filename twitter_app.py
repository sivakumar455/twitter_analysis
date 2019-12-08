
import tweepy
from wordcloud import WordCloud
import matplotlib.pyplot as plt

import logging

CONSUMER_KEY = "PASTE_YOUR_KEY"
CONSUMER_SECRET = "PASTE_YOUR_KEY"
ACCESS_TOKEN = "PASTE_YOUR_KEY"
ACCESS_TOKEN_SECRET = "PASTE_YOUR_KEY"

#logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class MyStreamListener(tweepy.StreamListener):
    def __init__(self,api):
        self.api = api
        self.me = api.me()

    def on_status(self,tweet):
        print("***********************")
        print(f"{tweet.user.name} : {tweet.text}")

    def on_error(self, status):
        logger.error(f"Error detected in tweet stream")


def create_api():

    # authenticate twitter
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # create API obj
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Failed to create tweet API")
        raise e

    logger.info("Successfully created tweet API")
    return api


def get_user(api, name):
    user = api.get_user(name)

    print("User details:")
    print(user.name)
    print(user.description)
    print(user.location)

    print("Last 20 Followers:")
    for follower in user.followers():
        print(follower.name)


def search_tweet(api, query):
    txt = ""

    lst = []

    for tweet in api.search(q=query, lang="en", count=50):
        #print("*******************************")
        #print(f"{tweet.user.name}::::{tweet.text}")
        #print(f"{tweet.text}")
        txt += tweet.text
        lst.append(tweet.text)

    return lst,txt


def trends(api):
    trend_results = api.trends_place(1)

    for trend in trend_results[0]["trends"]:
        print(trend["name"])


def display_wordcloud(tweet_text):
    wordcloud = WordCloud(width=480, height=480, max_font_size=50, min_font_size=10, margin=0).generate(tweet_text)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.margins(x=0, y=0)
    plt.show()


def display_timeline_tweets(api):
    timeline = api.home_timeline()
    for tweet in timeline:
        print(f"{tweet.user.name} ::: {tweet.text}" )


def update_tweet(msg):
    api.update_status(msg)


def run_stream(api, name):
    tweets_listener = MyStreamListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=[name], languages=["en"], is_async=True)



if __name__ == "__main__":
    api = create_api()

    #get_user(api, "byjus")
    tweet_text = search_tweet(api,"Amdocs")
    print(tweet_text)
    display_wordcloud(tweet_text)

    #trends(api)

    #display_timeline_tweets(api)

    #run_stream(api,"uber")
