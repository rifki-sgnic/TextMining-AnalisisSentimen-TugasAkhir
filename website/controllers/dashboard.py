from website.models import Models

class DashboardController:

    def getData(self):
        data = {}

        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_data_crawling')
        data['data_crawling'] = instance_model.select()[0]['jumlah']

        instance_model = Models('SELECT COUNT(id_slangword) as jumlah FROM tbl_slangword')
        data['data_slangword'] = instance_model.select()[0]['jumlah']
        
        instance_model = Models('SELECT COUNT(id_stopword) as jumlah FROM tbl_stopword')
        data['data_stopword'] = instance_model.select()[0]['jumlah']

        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean')
        data['data_preprocess'] = instance_model.select()[0]['jumlah']

        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment IS NOT NULL')
        data['data_berlabel'] = instance_model.select()[0]['jumlah']
        
        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_data_train WHERE sentiment IS NOT NULL')
        data['data_train'] = instance_model.select()[0]['jumlah']
        
        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_data_test WHERE sentiment IS NOT NULL')
        data['data_test'] = instance_model.select()[0]['jumlah']

        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment = "positif"')
        data['data_pos'] = instance_model.select()[0]['jumlah']

        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment = "negatif"')
        data['data_neg'] = instance_model.select()[0]['jumlah']

        return data