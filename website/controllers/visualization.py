import json

from flask import flash
from website.models import Models
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
import operator
import os


class VisualizationController:
    def createVisualisasi(self):
        waktu = datetime.today().strftime('%d-%m-%Y %H%M')
        
        try:
            instance_model =  Models('SELECT DATE(created_at) as tanggal FROM tbl_data_clean WHERE clean_text IS NOT NULL AND sentiment IS NOT NULL')
            distribusi_waktu = instance_model.select()

            list_tanggal = [str(data['tanggal']) for data in distribusi_waktu]

            plt.subplots(figsize=(25, 10))
            plt.hist(list_tanggal, bins=125)

            plt.ylabel('Jumlah Tweet', fontsize=18)
            plt.xlabel('Tanggal Perolehan', fontsize=18)
            plt.xticks(rotation=45)

            plt.grid()

            plt.savefig('website/static/visualisasi/histogram_dist_waktu.png')

            plt.cla()
            plt.clf()

            instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment = "positif"')
            count_pos = instance_model.select()[0]['jumlah']

            instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment = "negatif"')
            count_neg = instance_model.select()[0]['jumlah']

            jumlah_data = count_pos + count_neg
            persentase_pos = round((count_pos / jumlah_data) * 100, 2)
            persentase_neg = round((count_neg / jumlah_data) * 100, 2)

            list_countSentiment = [persentase_pos, persentase_neg]

            plt.subplots(figsize=(10, 10))
            plt.pie(list_countSentiment, labels=['Positif ('+ str(persentase_pos) +'%)', 'Negatif ('+ str(persentase_neg) +'%)'], colors=['#00c853', '#ff1744'], startangle=90)
            plt.legend(title="Data Tipe Sentimen")

            plt.savefig('website/static/visualisasi/pie_sentimen.png')

            plt.cla()
            plt.clf()

            instance_model = Models("SELECT clean_text FROM tbl_data_clean WHERE clean_text IS NOT NULL AND sentiment = 'positif'")
            data_positif = instance_model.select()
                
            instance_model = Models("SELECT clean_text FROM tbl_data_clean WHERE clean_text IS NOT NULL AND sentiment = 'negatif'")
            data_negatif = instance_model.select()

            string_positif = ""
            for data in data_positif:
                string_positif += str(data['clean_text']) + " "
                
            string_negatif = ""
            for data in data_negatif:
                string_negatif += str(data['clean_text']) + " "

            wordcloud = WordCloud(width=800, height=400, background_color='black', collocations=False).generate(string_positif)
            wordcloud.to_file('website/static/visualisasi/wordcloud_positif.png')

            wordcloud = WordCloud(width=800, height=400, background_color='black', collocations=False).generate(string_negatif)
            wordcloud.to_file('website/static/visualisasi/wordcloud_negatif.png')

        except:
            if os.path.exists('website/static/visualisasi/histogram_dist_waktu.png'):
                os.remove('website/static/visualisasi/histogram_dist_waktu.png')
            else:
                print('\nFile histogram tidak ditemukan')
            if os.path.exists('website/static/visualisasi/pie_sentimen.png'):
                os.remove('website/static/visualisasi/pie_sentimen.png')
            else:
                print('\nFile piechart tidak ditemukan')
            return {'error': 'Terjadi Kesalahan'}

        counts = {}
        for word in string_positif.split():
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
        frekuensi_pos = dict(sorted(counts.items(), key=operator.itemgetter(1), reverse=True))
        
        for word in string_negatif.split():
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
        frekuensi_neg = dict(sorted(counts.items(), key=operator.itemgetter(1), reverse=True))

        data = {
            'jumlah_tweets': len(list_tanggal),
            'jumlah_pos': count_pos,
            'jumlah_neg': count_neg,
            'persentase_pos': persentase_pos,
            'persentase_neg': persentase_neg,
            'frekuensi_pos': list(frekuensi_pos.items())[:15],
            'frekuensi_neg': list(frekuensi_neg.items())[:15],
            'waktu': waktu
        }

        # Menyimpan hasil visualisasi dalam bentuk json
        with open(os.path.join('website/static/visualisasi/', 'hasil_visualisasi.json'), 'w') as outfile:
            json.dump(data, outfile, indent=2)

        return 'true'

    def getVisualisasi(self):
        filepath = 'website/static/visualisasi/hasil_visualisasi.json'

        try:
            data = json.load(open(filepath))
        except:
            data = None
        
        return data


    def deleteVisualisasi(self):
        filepath = 'website/static/visualisasi/hasil_visualisasi.json'

        if os.path.exists(filepath):
            os.remove(filepath)
            flash('Berhasil menghapus data.', 'success')

        return None