from flask import flash, request
from website.excel import Excel
from website.models import Models


class KamusController:

    # Slangword
    def select_dataSlangword(self):
        instance_model = Models('SELECT * FROM tbl_slangword')
        slangword = instance_model.select()
        
        return slangword

    def add_dataSlangword(self):
        slangword = request.form['slangword'].strip()
        kata_asli = request.form['kata_asli'].strip()

        data_tambah = (slangword.lower(), kata_asli.lower())

        instance_model = Models('INSERT INTO tbl_slangword(slangword, kata_asli) VALUES (%s, %s)')
        instance_model.query_sql(data_tambah)
        flash('Berhasil menambahkan data.', 'success')
        return None

    def update_dataSlangword(self):
        id = request.form['id']
        slangword = request.form['slangword'].strip()
        kata_asli = request.form['kata_asli'].strip()

        data_ubah = (slangword.lower(), kata_asli.lower(), id)

        instance_model = Models('UPDATE tbl_slangword SET slangword=%s, kata_asli=%s WHERE id_slangword = %s')
        instance_model.query_sql(data_ubah)
        flash('Berhasil mengubah data.', 'success')
        return None

    def delete_dataSlangword(self):
        id = request.form['id']
        
        instance_model = Models('DELETE FROM tbl_slangword WHERE id_slangword=%s')
        instance_model.query_sql(id)
        flash('Berhasil menghapus data.', 'success')
        return None

    def delete_allDataSlangword(self):
        instance_model = Models('DELETE FROM tbl_slangword')
        instance_model.query_delete_all()
        return None

    def import_dataSlangword(self):
        excel_file = request.files['excel_file']

        if(excel_file.filename.lower().endswith(('.xls', '.xlsx'))):
            instance_excel = Excel()
            tuples_excel = instance_excel.make_tuples_slangwords(excel_file)

            instance_model = Models('INSERT INTO tbl_slangword(slangword, kata_asli) VALUES (%s, %s)')
            instance_model.query_sql_multiple(tuples_excel)
            flash('Berhasil import file!')
            return None
        flash('Format file tidak sesuai! Harus berekstensi .xls atau .xlsx')
        return None

    # Stopword
    def select_dataStopword(self):
        instance_model = Models('SELECT * FROM tbl_stopword')
        stopword = instance_model.select()
        
        return stopword

    def add_dataStopword(self):
        stopword = request.form['stopword'].strip()

        instance_model = Models('INSERT INTO tbl_stopword(stopword) VALUES (%s)')
        instance_model.query_sql(stopword.lower())
        flash('Berhasil menambahkan data.', 'success')
        return None

    def update_dataStopword(self):
        id = request.form['id']
        stopword = request.form['stopword'].strip()

        data_ubah = (stopword.lower(), id)

        instance_model = Models('UPDATE tbl_stopword SET stopword=%s WHERE id_stopword = %s')
        instance_model.query_sql(data_ubah)
        flash('Berhasil mengubah data.', 'success')
        return None

    def delete_dataStopword(self):
        id = request.form['id']
        
        instance_model = Models('DELETE FROM tbl_stopword WHERE id_stopword=%s')
        instance_model.query_sql(id)
        flash('Berhasil menghapus data.', 'success')
        return None

    def delete_allDataStopword(self):
        instance_model = Models('DELETE FROM tbl_stopword')
        instance_model.query_delete_all()
        return None

    def import_dataStopword(self):
        excel_file = request.files['excel_file']

        if(excel_file.filename.lower().endswith(('.xls', '.xlsx'))):
            instance_excel = Excel()
            tuples_excel = instance_excel.make_tuples_stopwords(excel_file)

            instance_model = Models('INSERT INTO tbl_stopword(stopword) VALUES (%s)')
            instance_model.query_sql_multiple(tuples_excel)
            flash('Berhasil import file!')
            return None
        flash('Format file tidak sesuai! Harus berekstensi .xls atau .xlsx')
        return None
