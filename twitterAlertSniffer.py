import psycopg2
import tweepy
from HTMLParser import HTMLParser
import json


def parsePlace(data):
    data = json.loads(HTMLParser().unescape(data))
    tweet = data['coordinates']
    print tweet
    return True

class DB:
	def __init__(self):
		self.conn = psycopg2.connect("dbname=hdmthon user=hdm password=17outubro2015 host=200.132.11.22 port=1305")
		self.cur = self.conn.cursor()
		self.conn.autocommit = True

	def save(self,tag,tweet,location):

		

		tag = "\'" + tag + "\'"
		tweet = "\'" + tweet + "\'"
		lon = "\'" + location[0]  + "\'"
		lat = "\'" + location[1]  + "\'"
		sql = "INSERT INTO twitter (tag, tweet, lon, lat) VALUES" + " (" + tag + "," +  tweet + "," + lon + "," +  lat +  ")"
		self.cur.execute(sql)


class MyStreamListener(tweepy.StreamListener):

	def __init__(self,words):
		self.words = words
	def on_status(self, status):


		#location = status.coordinates
		if status.place:
			place = status.place
			coordList = place.bounding_box.coordinates[0]

			lat = (coordList[0][0] + coordList[2][0]) / 2.0
			lon = (coordList[2][1] + coordList[3][1]) / 2.0
			print status.text

			tweet = status.text

			for word in self.words:
				if word.lower() in tweet.lower():
					print status.text, word
					theDB.save(word,status.text, (str(lon), str(lat)))


class TwitterHandler:

	def __init__(self,words):
		consumer_key="JAZRiVjf3vXSeDMZXNdBD7F3x"
		consumer_secret="RCvY9EPoIfHQ1MudzgFGPFemM5qe80vubKnbDaXZNovkUtMFOG"

		access_token="210847926-pzGf6NsmRXCr04NK32ruwEuM2hZ0Xt2e31Y4fBrq"
		access_token_secret="aZQ2Mq83xwzaceaoNeKzzXB8t5rbdFlVbaXMhurXZ6d41"

		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)

		self.api = tweepy.API(auth)

		
		theListener = MyStreamListener(words)
		theListener.api = self.api
		self.myStream = tweepy.Stream(auth = self.api.auth, listener=theListener)
		self.myStream.filter(track=words, async=True)

	def search(self,keyword,number):
		return self.api.search(q=keyword, count=number, geo=(-30.1088701,-51.1771419,40))
		 
theDB = DB()
if __name__ == '__main__':
	
	twitter = TwitterHandler(["chuva", "granizo", "alagamento", "enchente", "perigo", "emergencia"])

