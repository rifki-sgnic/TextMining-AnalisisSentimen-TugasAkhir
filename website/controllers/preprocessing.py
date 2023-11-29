from flask import request
from website.models import Models
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class PreprocessingController:

    def select_data_preprocessing(self):
        instance_model = Models('SELECT * FROM tbl_tweet_preprocessing')
        data_preprocessing = instance_model.select()
        return data_preprocessing

    def add_data_preprocessing(self):
        aksi = request.form['aksi']

        if aksi == 'preprocessing':
            instance_model = Models('SELECT * FROM tbl_tweet_crawling')
            data_preprocess = instance_model.select()

            save_data = []

            instance_model = Models('SELECT * FROM tbl_slangword')
            slangwords = instance_model.select()

            instance_model = Models('SELECT * FROM tbl_stopword')
            stopwords = instance_model.select()

            instance_stemming = StemmerFactory()
            stemmer = instance_stemming.create_stemmer()

            print('-- Mulai Proses '+ str(len(data_preprocess)) +' Data --')

            for index, data in enumerate(data_preprocess):
                result_text = data['text'].lower() # Casefolding
                casefold = result_text
                
                # Cleaning
                result_text = re.sub(r'http\S+|@\S+|#\S+|\d+', '', result_text) # Menghapus mention, hashtag, link
                result_text = re.sub(r'[^a-z ]', ' ', result_text)   # Mengubah karakter selain huruf a-z menjadi spasi
                result_text = result_text.strip()   # Menghapus spasi berlebih di akhir kata
                result_text = re.sub('\s+', ' ', result_text) # Menghapus spasi berlebih di antara kata
                cleansing = result_text
                
                # Change slangwords
                for slang in slangwords:
                    if slang['slangword'] in result_text:
                        result_text = re.sub(r'\b{}\b'.format(slang['slangword']), slang['kata_asli'], result_text)
                slangword = result_text
                
                # Remove stopwords
                for stop in stopwords:
                    if stop['stopword'] in result_text:
                        result_text = re.sub(r'\b{}\b'.format(stop['stopword']), '', result_text)
                stopword = result_text
                
                # Stemming
                result_text = stemmer.stem(result_text)
                stemming = result_text

                if result_text != '':
                    try:
                        save_data.append((data['id'], data['text'], casefold, cleansing, slangword, stopword, stemming, result_text, data['user'], data['created_at']))
                    except:
                        print('\nGagal Menyimpan Data (ID: '+ str(data['id']) +')\n')
                else:
                    print('\nGagal Menyimpan Data (ID: '+ str(data['id']) +')\n')
                    
                print('Data ke-'+ str(index+1))

            instance_model = Models('REPLACE INTO tbl_tweet_preprocessing(id, text, casefolding, cleansing, slangword, stopword, stemming, clean_text, user, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
            instance_model.query_sql_multiple(save_data)

            print('\n -- SELESAI -- ')

        return None
        
    
    def count_data_crawling(self):
        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_crawling')
        data_crawling = instance_model.select()
        return data_crawling[0]['jumlah']
    
    def count_data_preprocessing(self):
        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_preprocessing')
        data_preprocessing = instance_model.select()
        return data_preprocessing[0]['jumlah']

    
    def delete_all_preprocessing(self):
        instance_model = Models('DELETE FROM tbl_tweet_preprocessing')
        instance_model.query_delete_all()
        return None