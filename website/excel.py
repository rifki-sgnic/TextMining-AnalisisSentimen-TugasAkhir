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


    # Fungsi membuat tuple dari data excel slangword
    def make_tuples_slangwords(self, df):
        texts_container = []
        df = pd.read_excel(df)
        
        for index, row in df.iterrows():
            text_tuple = (str(row['slangwords']).lower(), str(row['kata asli']).lower())
            texts_container.append(text_tuple)
        
        return texts_container

    # Fungsi tuple dari data excel stopword
    def make_tuples_stopwords(self, df):
        texts_container = []
        df = pd.read_excel(df)

        for index, row in df.iterrows():
            text_tuple = (str(row['stopwords']).lower())
            texts_container.append(text_tuple)
        
        return texts_container

    # Fungsi tuple dari data excel kata positif
    def make_tuples_kata_positif(self, df):
        texts_container = []
        df = pd.read_excel(df)

        for index, row in df.iterrows():
            text_tuple = (str(row['positive_word']).lower())
            texts_container.append(text_tuple)

        return texts_container
    
    # Fungsi tuple dari data excel kata negatif
    def make_tuples_kata_negatif(self, df):
        texts_container = []
        df = pd.read_excel(df)

        for index, row in df.iterrows():
            text_tuple = (str(row['negative_word']).lower())
            texts_container.append(text_tuple)

        return texts_container
