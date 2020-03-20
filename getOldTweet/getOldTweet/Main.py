# -*- coding: utf-8 -*-

import got3 as got

def main():

	def printTweet(descr, t):
		print(descr)
		print("Username: %s" % t.username)
		print("Retweets: %d" % t.retweets)
		print("Text: %s" % t.text)
		print("Mentions: %s" % t.mentions)
		print("Hashtags: %s\n" % t.hashtags)

	# Example 1 - Get tweets by username
	tweetCriteria = got.manager.TweetCriteria().setUsername('barackobama').setMaxTweets(1)
	tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]

	printTweet("### Example 1 - Get tweets by username [barackobama]", tweet)

	# Example 2 - Get tweets by query search
	tweetCriteria = got.manager.TweetCriteria().setQuerySearch('europe refugees').setSince("2015-05-01").setUntil("2015-09-30").setMaxTweets(1)
	tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]

	printTweet("### Example 2 - Get tweets by query search [europe refugees]", tweet)

	# Example 3 - Get tweets by username and bound dates
	tweetCriteria = got.manager.TweetCriteria().setUsername("barackobama").setSince("2015-09-10").setUntil("2015-09-12").setMaxTweets(1)
	tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]

	printTweet("### Example 3 - Get tweets by username and bound dates [barackobama, '2015-09-10', '2015-09-12']", tweet)

if __name__ == '__main__':
	# main()

	def printTweet(descr, t):
		print(descr)
		print("ID: %s" % t.id)
		print("Username: %s" % t.username)
		print("Author ID: %s" % t.author_id)
		print("Text: %s" % t.text)
		print("Pictures: {}".format(", ".join(t.pics)))
		print("Mentions: {}".format(", ".join(t.mentions)))
		print("Hashtags: {}".format(" ".join(t.hashtags)))
		print("Urls: {}".format(", ".join(t.urls)))
		print("date: %s" % t.date.strftime('%Y-%m-%d %H:%M:%S'))
		print("formatted_date: {}".format(t.formatted_date))
		print("retweets: {}({})".format(t.retweets, type(t.retweets)))
		print("favorites: {}".format(t.favorites))
		print("geo: {}({})".format(t.geo, type(t.geo)))
		print("author_id: {}".format(t.author_id))

	tweetCriteria = got.manager.TweetCriteria().setQuerySearch('#joy').setLang('en').setSince("2016-11-14").setUntil("2016-11-15").setMaxTweets(1)
	tweets = got.manager.TweetManager.getTweets(tweetCriteria)

	print('### Get tweets by query search [#joy lang:en 20161115]')
	for i, tweet in enumerate(tweets):
		printTweet('#{}'.format(i+1), tweet)
		# try:
		# 	printTweet('#{}'.format(i+1), tweet)
		# except:
		# 	print('*** Error happens ***\n')
