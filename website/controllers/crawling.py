from flask import flash, request
from website.models import Models
from website.excel import Excel

class CrawlingController:

    def select_data_crawling(self):
        instance_model = Models('SELECT * FROM tbl_data_crawling')
        data_crawling = instance_model.select()
        return data_crawling


    def import_crawlingExcel(self):
        excel_file = request.files['excel_file']

        if(excel_file.filename.lower().endswith(('.xls', '.xlsx'))):
            instance_excel = Excel()
            tuples_excel = instance_excel.make_tuples_crawling(excel_file)

            instance_model = Models('REPLACE INTO tbl_data_crawling(id, text, user, created_at) VALUES (%s, %s, %s, %s)')
            instance_model.query_sql_multiple(tuples_excel)
            return None

        flash('Format tidak sesuai! Pastikan file ber-ekstensi .xls atau .xlsx', 'error')
        return None