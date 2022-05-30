from numpy import result_type
from website import api
from datetime import datetime, timezone

class Api:

    def search_tweet(self, keyword, tanggal_awal, tanggal_akhir):
        startDate = datetime.strptime(tanggal_awal, '%Y-%m-%d')
        startDate = startDate.replace(tzinfo=timezone.utc)
        endDate = datetime.strptime(tanggal_akhir, '%Y-%m-%d')
        endDate = endDate.replace(hour=23, minute=59, second=59, tzinfo=timezone.utc)

        tweets = []

        search = api.search_tweets(keyword + ' -filter:retweets', lang='id', result_type='recent', tweet_mode='extended')
        for tweet in search:
            if tweet.created_at < endDate and tweet.created_at > startDate:
                tweets.append(tweet._json)

        while(search[-1].created_at > startDate):
            print('Tweet @ - ', search[-1].created_at, ' - Diambil')
            search = api.search_tweets(keyword + ' -filter:retweets', lang='id', result_type='recent', tweet_mode='extended', max_id=search[-1].id)
            for tweet in search:
                if tweet.created_at < endDate and tweet.created_at > startDate and not tweet._json in tweets:
                    tweets.append(tweet._json)

        return tweets