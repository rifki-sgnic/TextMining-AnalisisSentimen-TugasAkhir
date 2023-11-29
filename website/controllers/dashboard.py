from website.models import Models

class DashboardController:

    def getData(self):
        data = {}

        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_crawling')
        data['data_crawling'] = instance_model.select()[0]['jumlah']

        instance_model = Models('SELECT COUNT(id_slangword) as jumlah FROM tbl_slangword')
        data['data_slangword'] = instance_model.select()[0]['jumlah']
        
        instance_model = Models('SELECT COUNT(id_stopword) as jumlah FROM tbl_stopword')
        data['data_stopword'] = instance_model.select()[0]['jumlah']

        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_preprocessing')
        data['data_preprocess'] = instance_model.select()[0]['jumlah']

        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_preprocessing WHERE label IS NOT NULL')
        data['data_berlabel'] = instance_model.select()[0]['jumlah']
        
        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_data_train WHERE label IS NOT NULL')
        data['data_train'] = instance_model.select()[0]['jumlah']
        
        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_data_test WHERE label IS NOT NULL')
        data['data_test'] = instance_model.select()[0]['jumlah']

        if data['data_train'] != 0 and data['data_test'] != 0:
            data['rasio_bagi_train'] = round(data['data_train'] / (data['data_train'] + data['data_test']), 2) * 10
            data['rasio_bagi_test'] = round(data['data_test'] / (data['data_train'] + data['data_test']), 2) * 10
        else:
            data['rasio_bagi_train'] = 0
            data['rasio_bagi_test'] = 0

        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_preprocessing WHERE label = "positif"')
        data['data_pos'] = instance_model.select()[0]['jumlah']

        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_preprocessing WHERE label = "negatif"')
        data['data_neg'] = instance_model.select()[0]['jumlah']

        return data