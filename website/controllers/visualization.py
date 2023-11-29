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
    def create_visualisasi(self):
        
        try:
            instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_preprocessing WHERE label = "positif"')
            count_pos = instance_model.select()[0]['jumlah']

            instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_preprocessing WHERE label = "negatif"')
            count_neg = instance_model.select()[0]['jumlah']

            jumlah_data = count_pos + count_neg
            persentase_pos = round((count_pos / jumlah_data) * 100, 2)
            persentase_neg = round((count_neg / jumlah_data) * 100, 2)

            list_countSentiment = [persentase_pos, persentase_neg]

            plt.subplots(figsize=(9, 9))
            plt.pie(list_countSentiment, 
                    labels=['Positif ('+ str(persentase_pos) +'%)', 'Negatif ('+ str(persentase_neg) +'%)'],
                    colors=['#00c853', '#ff1744'],
                    startangle=90)
            # draw circle
            centre_circle = plt.Circle((0, 0), 0.60, fc='white')
            fig = plt.gcf()
            # Adding Circle in Pie chart
            fig.gca().add_artist(centre_circle)
            
            plt.legend(title="Data Tipe Sentimen", loc="upper right")

            plt.savefig('website/static/visualisasi/pie_sentimen.png')

            plt.cla()
            plt.clf()

            instance_model = Models("SELECT clean_text FROM tbl_tweet_preprocessing WHERE clean_text IS NOT NULL AND label = 'positif'")
            data_positif = instance_model.select()
                
            instance_model = Models("SELECT clean_text FROM tbl_tweet_preprocessing WHERE clean_text IS NOT NULL AND label = 'negatif'")
            data_negatif = instance_model.select()

            string_positif = ""
            for data in data_positif:
                string_positif += str(data['clean_text']) + " "
                
            string_negatif = ""
            for data in data_negatif:
                string_negatif += str(data['clean_text']) + " "

            wordcloud = WordCloud(width=800, height=400, background_color='white', collocations=False).generate(string_positif)
            wordcloud.to_file('website/static/visualisasi/wordcloud_positif.png')

            wordcloud = WordCloud(width=800, height=400, background_color='white', collocations=False).generate(string_negatif)
            wordcloud.to_file('website/static/visualisasi/wordcloud_negatif.png')

        except:
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
            'jumlah_pos': count_pos,
            'jumlah_neg': count_neg,
            'persentase_pos': persentase_pos,
            'persentase_neg': persentase_neg,
            'frekuensi_pos': list(frekuensi_pos.items())[:15],
            'frekuensi_neg': list(frekuensi_neg.items())[:15]
        }

        # Menyimpan hasil visualisasi dalam bentuk json
        with open(os.path.join('website/static/visualisasi/', 'hasil_visualisasi.json'), 'w') as outfile:
            json.dump(data, outfile, indent=2)

        return 'true'

    def get_visualisasi(self):
        filepath = 'website/static/visualisasi/hasil_visualisasi.json'

        try:
            data = json.load(open(filepath))
        except:
            data = None
        
        return data


    def delete_visualisasi(self):
        filepath = 'website/static/visualisasi/hasil_visualisasi.json'

        if os.path.exists(filepath):
            os.remove(filepath)
            flash('Berhasil menghapus data.', 'success')

        return None