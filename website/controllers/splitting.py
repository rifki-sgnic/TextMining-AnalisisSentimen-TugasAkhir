import math
import random
from flask import request
from website.models import Models


class SplittingController:

    def count_dataWithLabel(self):
        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_clean WHERE sentiment_type IS NOT NULL')
        data_labeling = instance_model.select()
        return data_labeling[0]['jumlah']

    def select_dataTrain(self):
        instance_model = Models('SELECT * FROM tbl_tweet_training')
        data_train = instance_model.select()
        return data_train

    def select_dataTest(self):
        instance_model = Models('SELECT * FROM tbl_tweet_testing')
        data_test = instance_model.select()
        return data_test

    def delete_allDataSplit(self):
        instance_model = Models('DELETE FROM tbl_tweet_training')
        instance_model.query_delete_all()
        instance_model = Models('DELETE FROM tbl_tweet_testing')
        instance_model.query_delete_all()
        return None

    def add_dataSplit(self):
        rasio = request.form['rasio']
        jumlah_data = float(request.form['jumlah_data'])

        if rasio == '1:9':
            jumlah_dataTest = math.floor(jumlah_data * 0.1)
            jumlah_dataTrain = math.ceil(jumlah_data * 0.9)
        elif rasio == '2:8':
            jumlah_dataTest = math.floor(jumlah_data * 0.2)
            jumlah_dataTrain = math.ceil(jumlah_data * 0.8)

        # Split data train lalu latih
        # value 0 = Data Test || value 1 = Data Train
        data_flag = []
        for i in range(int(jumlah_data)):
            if i < jumlah_dataTrain:
                data_flag.append(1)
            else:
                data_flag.append(0)
        
        # Random list data split
        random.shuffle(data_flag)

        # Select data tweet berlabel
        instance_model = Models('SELECT * FROM tbl_tweet_clean WHERE sentiment_type IS NOT NULL')
        data_withLabel = instance_model.select()

        data_simpan_train = []
        data_simpan_test = []

        for index, data in enumerate(data_withLabel):
            if data_flag[index] == 0:
                data_simpan_test.append((data['id'], data['text'], data['clean_text'], data['user'], data['created_at'], data['sentiment_type']))
            else :
                data_simpan_train.append((data['id'], data['text'], data['clean_text'], data['user'], data['created_at'], data['sentiment_type']))

        instance_model = Models('INSERT IGNORE tbl_tweet_testing(id, text, clean_text, user, created_at, sentiment_type) VALUES (%s, %s, %s, %s, %s, %s)')
        instance_model.query_sql_multiple(data_simpan_test)

        instance_model = Models('INSERT IGNORE tbl_tweet_training(id, text, clean_text, user, created_at, sentiment_type) VALUES (%s, %s, %s, %s, %s, %s)')
        instance_model.query_sql_multiple(data_simpan_train)

        return 'true'