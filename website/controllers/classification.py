from sklearn.metrics import confusion_matrix
from website.models import Models
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelBinarizer
from flask import flash, json
import pickle
import os

from website.multinb import MultiNB


class ClassificationController:
    def createModel(self):

        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_data_train WHERE clean_text IS NOT NULL AND sentiment IS NOT NULL')
        sentiment_count = instance_model.select()

        instance_model = Models("SELECT COUNT(id) as positif FROM tbl_data_train WHERE clean_text IS NOT NULL AND sentiment = 'positif'")
        sentiment_positif = instance_model.select()

        instance_model = Models("SELECT COUNT(id) as negatif FROM tbl_data_train WHERE clean_text IS NOT NULL AND sentiment = 'negatif'")
        sentiment_negatif = instance_model.select()

        # Data Training
        list_text_training = []
        list_label_training = []

        instance_model = Models('SELECT clean_text, sentiment FROM tbl_data_train')
        data_train = instance_model.select()

        for i in range(len(data_train)):
            list_text_training.append(data_train[i]['clean_text'])
            list_label_training.append(data_train[i]['sentiment'])

        # Data Testing
        list_text_testing = []
        list_label_testing = []

        instance_model = Models('SELECT clean_text, sentiment FROM tbl_data_test')
        data_test = instance_model.select()

        for i in range(len(data_test)):
            list_text_testing.append(data_test[i]['clean_text'])
            list_label_testing.append(data_test[i]['sentiment'])

        # Vectorize X_train X_test
        vectorizer = TfidfVectorizer()
        X_train = vectorizer.fit_transform(list_text_training).toarray()
        X_test = vectorizer.transform(list_text_testing).toarray()

        vocab = vectorizer.get_feature_names_out()

        # Vectorize y_train y_test
        labelBinarizer = LabelBinarizer()
        y_train = labelBinarizer.fit_transform(list_label_training).ravel()
        y_test = labelBinarizer.transform(list_label_testing).ravel()

        label = labelBinarizer.classes_

        # TRAIN MULTINOMIAL NAIVE BAYES
        model = MultiNB()
        model.fit(X_train, y_train)

        # SAVE MODEL as PKL
        filename = 'mnb_model.pkl'
        path = 'website/static/model_data/'
        with open(os.path.join(path, filename), 'wb') as out_name:
            pickle.dump(model, out_name, pickle.HIGHEST_PROTOCOL)

        # EVALUATION
        y_pred = model.predict(X_test)

        # Mengambil hasil prediksi label
        list_label_prediksi = []

        for i in range(len(y_pred)):
            if y_pred[i] == 0:
                list_label_prediksi.append("negatif")
            elif y_pred[i] == 1:
                list_label_prediksi.append("positif")

        # Mengambil hasil probabilitas prediksi label
        list_prob_prediksi = []

        predict_prob = model.predict_proba
        for i in range(len(predict_prob)):
            if predict_prob[i][0] > predict_prob[i][1]:
                list_prob_prediksi.append(predict_prob[i][0])
            else:
                list_prob_prediksi.append(predict_prob[i][1])

        true_neg, false_pos, false_neg, true_pos = confusion_matrix(y_test, y_pred).ravel()

        akurasi = (true_pos + true_neg) / (true_pos + true_neg + false_pos + false_neg)
        presisi = true_pos / (true_pos + false_pos)
        recall = true_pos / (true_pos + false_neg)

        data_dict = {
            "text_list" : list_text_testing,
            "label_list" : list_label_testing,
            "predict_label" : list_label_prediksi,
            "prob_predict" : list_prob_prediksi,
            "tp" : int(true_pos),
            "tn" : int(true_neg),
            "fp" : int(false_pos),
            "fn" : int(false_neg),
            "akurasi" : round(float(akurasi), 2),
            "presisi" : round(float(presisi), 2),
            "recall" : round(float(recall), 2)
        }

        # Menyimpan hasil evaluasi dalam bentuk json
        with open(os.path.join(path, 'hasil_evaluasi_model.json'), 'w') as outfile:
            json.dump(data_dict, outfile, indent=2)

        flash('Berhasil melakukan klasifikasi data.', 'success')

        return 'true'

    def getEvaluation(self):
        path = 'website/static/model_data/'
        filename = 'hasil_evaluasi_model.json'
        
        try:
            data = json.load(open(path+filename))
        except:
            data = None
        
        return data


    def deleteEvalutaion(self):
        filepath = 'website/static/model_data/hasil_evaluasi_model.json'

        if os.path.exists(filepath):
            os.remove(filepath)
            flash('Berhasil menghapus data.', 'success')

        return None