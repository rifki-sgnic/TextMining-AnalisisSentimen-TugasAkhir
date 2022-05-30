import pandas as pd
from datetime import datetime

class Excel:
    def __init__(self):
        self.file_excel_crawling = 'website/static/data_excel/data_crawling('+ datetime.today().strftime('%d-%m-%Y') +').xslx'

    def make_tuples_crawling(self, df=None):
        if df is None:
            df = pd.read_excel(self.file_excel_crawling)
        else:
            df = pd.read_excel(df)

        tweets_container = []
        for index, row in df.iterrows():
            try:
                tweet_tuple = (row['id'], str(row['text']), str(row['username']), str(datetime.strftime(datetime.strptime(row['created_at'],'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')))
            except:
                tweet_tuple = (row['id'], str(row['text']), str(row['username']), str(row['created_at']))
            tweets_container.append(tweet_tuple)

        return tweets_container

    # Fungsi menyimpan data_crawling dalam file excel (.xlsx)
    def save_crawling_excel(self, tweets):
        id = []
        text = []
        username = []
        created_at = []

        for tweet in tweets():
            id.append(tweet['id'])
            text.append(str(tweet['full_text']))
            username.append(str(tweet['user']['screen_name']))
            created_at.append(str(tweet['created_at']))

        df = pd.DataFrame({'id': id, 'text': text, 'username': username, 'created_at': created_at})
        df.to_excel(self.file_excel_crawling, index=False)

        print('File excel telah dibuat di lokasi: /:root_project/' + self.file_excel_crawling)
        return None

    # Fungsi membuat tuple dari data excel slangword
    def make_tuples_slangwords(self, df):
        tweets_container = []
        df = pd.read_excel(df)
        
        for index, row in df.iterrows():
            tweet_tuple = (str(row['slangwords']).lower(), str(row['kata asli']).lower())
            tweets_container.append(tweet_tuple)
        
        return tweets_container

    # Fungsi tuple dari data excel stopword
    def make_tuples_stopwords(self, df):
        tweets_container = []
        df = pd.read_excel(df)

        for index, row in df.iterrows():
            tweet_tuple = (str(row['stopwords']).lower())
            tweets_container.append(tweet_tuple)
        
        return tweets_container