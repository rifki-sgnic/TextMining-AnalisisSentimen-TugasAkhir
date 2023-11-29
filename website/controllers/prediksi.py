from flask import flash, request, json
from sklearn.feature_extraction.text import CountVectorizer
from website.multinb import MultiNB
import os
import pickle

class PrediksiController:
    def prediksi_teks(self):
        teks_prediksi = request.form['teks-prediksi']
        teks = [teks_prediksi]
        vectorizer = CountVectorizer()
        X_test = vectorizer.transform(teks).toarray()

        model = MultiNB()
        model = self.read_model("mnb_model.pkl", path='website/static/model_data/')

        y_pred = model.predict(X_test)
        return json.dumps({'predict' : y_pred})

    def read_model(self, filename, path=""):
        with open(os.path.join(path, filename), 'rb') as in_name:
            model = pickle.load(in_name)
            return model