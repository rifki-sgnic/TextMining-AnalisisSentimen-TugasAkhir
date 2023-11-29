from flask import flash, request
from website.models import Models
from website.excel import Excel

class CrawlingController:

    def select_data_crawling(self):
        instance_model = Models('SELECT * FROM tbl_tweet_crawling')
        data_crawling = instance_model.select()
        
        return data_crawling

    def count_data_crawling(self):
        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_crawling')
        count_data_crawling = instance_model.select()[0]['jumlah']

        return count_data_crawling

    def import_crawling_excel(self):
        excel_file = request.files['excel_file']

        if(excel_file.filename.lower().endswith(('.xls', '.xlsx'))):
            instance_excel = Excel()
            tuples_excel = instance_excel.make_tuples_crawling(excel_file)

            instance_model = Models('REPLACE INTO tbl_tweet_crawling(id, text, user, created_at) VALUES (%s, %s, %s, %s)')
            instance_model.query_sql_multiple(tuples_excel)
            return None

        flash('Format tidak sesuai! Pastikan file ber-ekstensi .xls atau .xlsx', 'error')
        return None

    def delete_data_crawling(self):
        instance_model = Models('DELETE FROM tbl_tweet_crawling')
        instance_model.query_delete_all()
        return None