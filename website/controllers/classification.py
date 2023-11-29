from sklearn.metrics import confusion_matrix
from website.models import Models
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from flask import flash, json
import pickle
import os

from website.multinb import MultiNB


class ClassificationController:
    def create_model(self):

        # Data Training
        list_text_training = []
        list_label_training = []

        instance_model = Models('SELECT clean_text, label FROM tbl_data_train')
        data_train = instance_model.select()

        for i in range(len(data_train)):
            list_text_training.append(data_train[i]['clean_text'])
            list_label_training.append(data_train[i]['label'])

        # Data Testing
        list_text_testing = []
        list_label_testing = []
        list_text_asli_testing = []

        instance_model = Models('SELECT text, clean_text, label FROM tbl_data_test')
        data_test = instance_model.select()

        for i in range(len(data_test)):
            list_text_asli_testing.append(data_test[i]['text'])
            list_text_testing.append(data_test[i]['clean_text'])
            list_label_testing.append(data_test[i]['label'])

        # Vectorize X_train X_test
        vectorizer = CountVectorizer()
        X_train = vectorizer.fit_transform(list_text_training).toarray()
        X_test = vectorizer.transform(list_text_testing).toarray()

        # Vectorize y_train y_test
        labelEncoder = LabelEncoder()
        y_train = labelEncoder.fit_transform(list_label_training).ravel()
        y_test = labelEncoder.transform(list_label_testing).ravel()

        # TRAIN MULTINOMIAL NAIVE BAYES
        model = MultiNB()
        model.fit(X_train, y_train)

        # SAVE MODEL as PKL
        # filename = 'mnb_model.pkl'
        # path = 'website/static/model_data/'
        # with open(os.path.join(path, filename), 'wb') as out_name:
        #     pickle.dump(model, out_name, pickle.HIGHEST_PROTOCOL)

        # PREDICT
        y_pred = model.predict(X_test)

        # Mengambil nilai probabilitas prediksi label
        list_prob_prediksi = []
        
        predict_prob = model.predict_prob
        for i in range(len(predict_prob)):
            tuple_pred = (round(float(predict_prob[i][0]), 3), round(float(predict_prob[i][1]), 3), round(float(predict_prob[i][2]), 3))
            list_prob_prediksi.append(tuple_pred)

        # Mengambil hasil prediksi label
        list_label_prediksi = []

        for i in range(len(y_pred)):
            if y_pred[i] == 0:
                list_label_prediksi.append("negatif")
            elif y_pred[i] == 1:
                list_label_prediksi.append("netral")
            elif y_pred[i] == 2:
                list_label_prediksi.append("positif")

        jumlah_kelas = len(labelEncoder.classes_)

        if (jumlah_kelas > 2):
            conf_mat = confusion_matrix(y_test, y_pred)

            TNeg = conf_mat[0][0]
            FNeg1 = conf_mat[0][1]
            FNeg2 = conf_mat[0][2]
            FNet1 = conf_mat[1][0]
            TNet = conf_mat[1][1]
            FNet2 = conf_mat[1][2]
            FPos1 = conf_mat[2][0]
            FPos2 = conf_mat[2][1]
            TPos = conf_mat[2][2]

            akurasi3kelas = (TNeg + TNet + TPos) / (TNeg + FNeg1 + FNeg2 + FNet1 + TNet + FNet2 + FPos1 + FPos2 + TPos)

            presisi_negatif = TNeg / (TNeg + FNet1 + FPos1)
            presisi_netral = TNet / (TNet + FNeg1 + FPos2)
            presisi_positif = TPos / (TPos + FNeg2 + FNet2)
            presisi3kelas = (presisi_negatif + presisi_netral + presisi_positif) / len(labelEncoder.classes_)

            recall_negatif = TNeg / (TNeg + FNeg1 + FNeg2)
            recall_netral = TNet / (TNet + FNet1 + FNet2)
            recall_positif = TPos / (TPos + FPos1 + FPos2)
            recall3kelas = (recall_negatif + recall_netral + recall_positif) / len(labelEncoder.classes_)

            data_dict = {
                "text_list" : list_text_testing,
                "text_asli_list": list_text_asli_testing,
                "label_list" : list_label_testing,
                "predict_label" : list_label_prediksi,
                "predict_prob" : list_prob_prediksi,
                "tneg" : int(TNeg),
                "fneg1" : int(FNeg1),
                "fneg2" : int(FNeg2),
                "fnet1" : int(FNet1),
                "tnet" : int(TNet),
                "fnet2" : int(FNet2),
                "fpos1" : int(FPos1),
                "fpos2" : int(FPos2),
                "tpos" : int(TPos),
                "jumlah_kelas" : int(jumlah_kelas),
                "presisi_negatif" : round(float(presisi_negatif), 2),
                "presisi_netral" : round(float(presisi_netral), 2),
                "presisi_positif" : round(float(presisi_positif), 2),
                "recall_negatif" : round(float(recall_negatif), 2),
                "recall_netral" : round(float(recall_netral), 2),
                "recall_positif" : round(float(recall_positif), 2),
                "akurasi" : round(float(akurasi3kelas), 2),
                "presisi" : round(float(presisi3kelas), 2),
                "recall" : round(float(recall3kelas), 2)
            }
        else:
            true_neg, false_pos, false_neg, true_pos = confusion_matrix(y_test, y_pred).ravel()

            akurasi = (true_pos + true_neg) / (true_pos + true_neg + false_pos + false_neg)
            presisi = true_pos / (true_pos + false_pos)
            recall = true_pos / (true_pos + false_neg)

            data_dict = {
                "text_list" : list_text_testing,
                "text_asli_list": list_text_asli_testing,
                "label_list" : list_label_testing,
                "predict_label" : list_label_prediksi,
                "predict_prob" : list_prob_prediksi,
                "tp" : int(true_pos),
                "tn" : int(true_neg),
                "fp" : int(false_pos),
                "fn" : int(false_neg),
                "jumlah_kelas" : int(jumlah_kelas),
                "akurasi" : round(float(akurasi), 2),
                "presisi" : round(float(presisi), 2),
                "recall" : round(float(recall), 2)
            }

        
        # Menyimpan hasil evaluasi dalam bentuk json
        path = 'website/static/model_data/'
        with open(os.path.join(path, 'hasil_evaluasi_model.json'), 'w') as outfile:
            json.dump(data_dict, outfile, indent=2)

        flash('Berhasil melakukan klasifikasi dan evaluasi data.', 'success')

        return 'true'

    def count_data_train(self):
        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_data_train')
        data_train = instance_model.select()
        return data_train[0]['jumlah']

    def get_evaluation(self):
        path = 'website/static/model_data/'
        filename = 'hasil_evaluasi_model.json'
        
        try:
            data = json.load(open(path+filename))
        except:
            data = None
        
        return data


    def delete_evalutaion(self):
        filepath = 'website/static/model_data/hasil_evaluasi_model.json'

        if os.path.exists(filepath):
            os.remove(filepath)
            flash('Berhasil menghapus data.', 'success')

        return None