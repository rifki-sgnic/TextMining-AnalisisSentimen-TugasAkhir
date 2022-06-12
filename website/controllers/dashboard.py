from website.models import Models

class DashboardController:

    def getData(self):
        data = {}

        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_crawling')
        data['data_crawling'] = instance_model.select()[0]['jumlah']

        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_clean')
        data['data_preprocess'] = instance_model.select()[0]['jumlah']

        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_clean WHERE sentiment_type IS NOT NULL')
        data['data_berlabel'] = instance_model.select()[0]['jumlah']
        
        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_training WHERE sentiment_type IS NOT NULL')
        data['data_train'] = instance_model.select()[0]['jumlah']
        
        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_testing WHERE sentiment_type IS NOT NULL')
        data['data_test'] = instance_model.select()[0]['jumlah']

        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_clean WHERE sentiment_type = "positif"')
        data['data_pos'] = instance_model.select()[0]['jumlah']

        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_clean WHERE sentiment_type = "negatif"')
        data['data_neg'] = instance_model.select()[0]['jumlah']

        return data