from flask import flash, request, json
from website.models import Models


class LabelingController:

    def select_dataWithLabel(self):
        instance_model = Models('SELECT * FROM tbl_tweet_preprocessing WHERE label IS NOT NULL')
        data_withLabel = instance_model.select()
        return data_withLabel

    def select_dataNoLabel(self):
        instance_model = Models('SELECT id, text, clean_text FROM tbl_tweet_preprocessing WHERE label IS NULL')
        data_noLabel = instance_model.select()
        return data_noLabel

    def count_data_with_label(self):
        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_preprocessing WHERE label IS NOT NULL')
        data_withLabel = instance_model.select()
        return data_withLabel[0]['jumlah']

    def add_dataLabeling(self):
        id = request.form['id']
        value = request.form['value']

        data_ubah = (value, id)
        instance_model = Models('UPDATE tbl_tweet_preprocessing SET label = %s WHERE id = %s')
        instance_model.query_sql(data_ubah)
        print(value)
        
        return 'Berhasil melabeli data.'

    def delete_dataLabeling(self):
        value = None
        instance_model = Models('UPDATE tbl_tweet_preprocessing SET label = %s WHERE label IS NOT NULL')
        instance_model.query_sql((value, ))
        flash('Berhasil menghapus data.', 'success')

        return None
        
        