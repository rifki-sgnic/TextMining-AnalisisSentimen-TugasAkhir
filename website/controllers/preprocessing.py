from flask import request, json
from website.models import Models
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class PreprocessingController:

    def select_dataPreprocessing(self):
        instance_model = Models('SELECT * FROM tbl_tweet_clean')
        data_preprocessing = instance_model.select()
        return data_preprocessing

    def add_dataPreprocessing(self):
        aksi = request.form['aksi']

        if aksi == 'preprocessing':
            instance_model = Models('SELECT * FROM tbl_tweet_crawling')
            data_preprocess = instance_model.select()

            first_data = []
            last_data = []
            casefolding = []
            remove_non_char = []
            remove_stopword = []
            change_slangword = []
            change_stemming = []

            save_data = []

            instance_model = Models('SELECT * FROM tbl_slangword')
            slangwords = instance_model.select()

            instance_model = Models('SELECT * FROM tbl_stopword')
            stopwords = instance_model.select()

            instance_stemming = StemmerFactory()
            stemmer = instance_stemming.create_stemmer()

            print('-- Proses '+ str(len(data_preprocess)) +' Data --')

            for index, data in enumerate(data_preprocess):
                first_data.append(data['text'])

                result_text = data['text'].lower() # Casefolding
                casefolding.append(result_text)
                
                # Cleaning
                result_text = re.sub(r'http\S+|@\S+|#\S+|\d+', '', result_text) # Menghapus mention, hashtag, link
                result_text = re.sub(r'[^a-z ]', '', result_text)   # Menghapus karakter selain huruf a-z
                result_text = result_text.strip()   # Menghapus spasi berlebih di akhir kata
                result_text = re.sub('\s+', ' ', result_text) # Menghapis spasi berlebih di antara kata
                remove_non_char.append(result_text)
                
                # Change slangwords
                for slang in slangwords:
                    if slang['slangword'] in result_text:
                        result_text = re.sub(r'\b{}\b'.format(slang['slangword']), slang['kata_asli'], result_text)
                change_slangword.append(result_text)
                
                # Remove stopwords
                for stop in stopwords:
                    if stop['stopword'] in result_text:
                        result_text = re.sub(r'\b{}\b'.format(stop['stopword']), '', result_text)
                remove_stopword.append(result_text)
                
                # Stemming
                result_text = stemmer.stem(result_text)
                change_stemming.append(result_text)

                last_data.append(result_text)
                
                if result_text != '':
                    try:
                        save_data.append((data['id'], data['text'], result_text, data['user'], data['created_at']))
                    except:
                        print('\nGagal Menyimpan Data (ID: '+ str(data['id']) +')\n')
                else:
                    print('\nGagal Menyimpan Data (ID: '+ str(data['id']) +')\n')
                    
                print('Data ke-'+ str(index+1))

            instance_model = Models('REPLACE INTO tbl_tweet_clean(id, text, clean_text, user, created_at) VALUES (%s, %s, %s, %s, %s)')
            instance_model.query_sql_multiple(save_data)

            print('\n -- SELESAI -- ')

        return json.dumps({'first_data': first_data, 'casefolding': casefolding, 'remove_non_char': remove_non_char, 'change_slangword': change_slangword, 'remove_stopword': remove_stopword, 'change_stemming': change_stemming, 'last_data': last_data})
        
    
    def count_dataCrawling(self):
        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_crawling')
        data_crawling = instance_model.select()
        return data_crawling[0]['jumlah']

    
    def delete_allDataPreprocess():
        instance_model = Models('DELETE FROM tbl_tweet_clean WHERE sentiment_type IS NULL')
        instance_model.query_delete_all()
        return None