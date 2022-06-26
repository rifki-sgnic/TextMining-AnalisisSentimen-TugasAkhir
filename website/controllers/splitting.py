from datetime import datetime
import math
import random
from flask import request
import pandas as pd
from website.models import Models


class SplittingController:

    def count_dataWithLabel(self):
        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment IS NOT NULL')
        data_labeling = instance_model.select()
        return data_labeling[0]['jumlah']

    def count_dataWithLabelPos(self):
        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment = "positif"')
        data_pos = instance_model.select()
        return data_pos[0]['jumlah']
    
    def count_dataWithLabelNeg(self):
        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment = "negatif"')
        data_neg = instance_model.select()
        return data_neg[0]['jumlah']

    def select_dataTrain(self):
        instance_model = Models('SELECT * FROM tbl_data_train')
        data_train = instance_model.select()
        return data_train

    def select_dataTest(self):
        instance_model = Models('SELECT * FROM tbl_data_test')
        data_test = instance_model.select()
        return data_test

    def delete_allDataSplit(self):
        instance_model = Models('DELETE FROM tbl_data_train')
        instance_model.query_delete_all()
        instance_model = Models('DELETE FROM tbl_data_test')
        instance_model.query_delete_all()
        return None

    def add_dataSplit(self):
        rasio = request.form['rasio']

        if rasio == '1:9':
            rasio_train = 0.9

        elif rasio == '2:8':
            rasio_train = 0.8

        # Select data tweet berlabel
        instance_model = Models('SELECT * FROM tbl_data_clean WHERE sentiment IS NOT NULL')
        data_withLabel = instance_model.select()

        df = pd.DataFrame(data_withLabel)

        # Membagi data train dan test dengan Stratified Sampling (Rasio label pada data latih dan uji sesuai dengan rasio label sebelum split data)
        train = df.groupby('sentiment', group_keys=False).apply(lambda x: x.sample(frac=rasio_train))
        test = df.drop(train.index)

        data_simpan_train = []
        data_simpan_test = []

        for index, data in train.iterrows():
            train_tuples = (data['id'], data['text'], data['clean_text'], data['user'], str(datetime.strftime(datetime.strptime(str(data['created_at']),'%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')), data['sentiment'])
            data_simpan_train.append(train_tuples)

        instance_model = Models('INSERT IGNORE tbl_data_train(id, text, clean_text, user, created_at, sentiment) VALUES (%s, %s, %s, %s, %s, %s)')
        instance_model.query_sql_multiple(data_simpan_train)

        for index, data in test.iterrows():
            test_tuples = (data['id'], data['text'], data['clean_text'], data['user'], str(datetime.strftime(datetime.strptime(str(data['created_at']),'%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')), data['sentiment'])
            data_simpan_test.append(test_tuples)

        instance_model = Models('INSERT IGNORE tbl_data_test(id, text, clean_text, user, created_at, sentiment) VALUES (%s, %s, %s, %s, %s, %s)')
        instance_model.query_sql_multiple(data_simpan_test)

        return 'true'