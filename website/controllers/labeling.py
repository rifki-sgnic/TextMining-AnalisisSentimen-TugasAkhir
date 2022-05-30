from flask import request, json
from website.models import Models


class LabelingController:

    def select_dataWithLabel(self):
        instance_model = Models('SELECT * FROM tbl_tweet_clean WHERE sentiment_type IS NOT NULL')
        data_withLabel = instance_model.select()
        return data_withLabel

    def select_dataNoLabel(self):
        instance_model = Models('SELECT id, text, clean_text FROM tbl_tweet_clean WHERE sentiment_type IS NULL')
        data_noLabel = instance_model.select()
        return data_noLabel

    def count_dataWithLabel(self):
        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_clean WHERE sentiment_type IS NOT NULL')
        data_withLabel = instance_model.select()
        return data_withLabel[0]['jumlah']

    def add_dataLabeling(self):
        id = request.form['id']
        value = request.form['value']

        data_ubah = (value, id)
        instance_model = Models('UPDATE tbl_tweet_clean SET sentiment_type = %s WHERE id = %s')
        instance_model.query_sql(data_ubah)
        return 'Berhasil melabeli data!'
        
        