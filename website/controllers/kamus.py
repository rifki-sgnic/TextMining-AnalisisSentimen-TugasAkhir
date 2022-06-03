from flask import flash, request
from website.excel import Excel
from website.models import Models


class KamusController:

    # Positif
    def select_dataKataPositif(self):
        instance_model = Models('SELECT * FROM tbl_lexicon_positive')
        data_positif = instance_model.select()
        return data_positif

    def add_dataKataPositif(self):
        kata_positif = request.form['kata_positif'].strip()

        instance_model = Models('INSERT INTO tbl_lexicon_positive(positive_word) VALUES (%s)')
        instance_model.query_sql(kata_positif.lower())
        flash('Berhasil menambahkan data.', 'success')
        return None

    def update_dataKataPositif(self):
        id = request.form['id']
        kata_positif = request.form['kata_positif'].strip()

        data_ubah = (kata_positif.lower(), id)

        instance_model = Models('UPDATE tbl_lexicon_positive SET positive_word=%s WHERE id_positive = %s')
        instance_model.query_sql(data_ubah)
        flash('Berhasil mengubah data.', 'success')
        return None

    def delete_dataKataPositif(self):
        id = request.form['id']
        
        instance_model = Models('DELETE FROM tbl_lexicon_positive WHERE id_positive=%s')
        instance_model.query_sql(id)
        flash('Berhasil menghapus data.', 'success')
        return None

    def delete_allDataKataPositif(self):
        instance_model = Models('DELETE FROM tbl_lexicon_positive')
        instance_model.query_delete_all()
        return None

    def import_dataKataPositif(self):
        excel_file = request.files['excel_file']

        if(excel_file.filename.lower().endswith(('.xls', '.xlsx'))):
            instance_excel = Excel()
            tuples_excel = instance_excel.make_tuples_kata_positif(excel_file)

            instance_model = Models('INSERT INTO tbl_lexicon_positive(positive_word) VALUES (%s)')
            instance_model.query_sql_multiple(tuples_excel)
            flash('Berhasil import file!')
            return None
        flash('Format file tidak sesuai! Harus berekstensi .xls atau .xlsx')
        return None
    
    # Negatif
    def select_dataKataNegatif(self):
        instance_model = Models('SELECT * FROM tbl_lexicon_negative')
        data_negatif = instance_model.select()

        return data_negatif

    def add_dataKataNegatif(self):
        kata_negatif = request.form['kata_negatif'].strip()

        instance_model = Models('INSERT INTO tbl_lexicon_negative(negative_word) VALUES (%s)')
        instance_model.query_sql(kata_negatif.lower())
        flash('Berhasil menambahkan data.', 'success')
        return None

    def update_dataKataNegatif(self):
        id = request.form['id']
        kata_negatif = request.form['kata_negatif'].strip()

        data_ubah = (kata_negatif.lower(), id)

        instance_model = Models('UPDATE tbl_lexicon_negative SET negative_word=%s WHERE id_negative = %s')
        instance_model.query_sql(data_ubah)
        flash('Berhasil mengubah data.', 'success')
        return None

    def delete_dataKataNegatif(self):
        id = request.form['id']
        
        instance_model = Models('DELETE FROM tbl_lexicon_negative WHERE id_negative=%s')
        instance_model.query_sql(id)
        flash('Berhasil menghapus data.', 'success')
        return None

    def delete_allDataKataNegatif(self):
        instance_model = Models('DELETE FROM tbl_lexicon_negative')
        instance_model.query_delete_all()
        return None

    def import_dataKataNegatif(self):
        excel_file = request.files['excel_file']

        if(excel_file.filename.lower().endswith(('.xls', '.xlsx'))):
            instance_excel = Excel()
            tuples_excel = instance_excel.make_tuples_kata_negatif(excel_file)

            instance_model = Models('INSERT INTO tbl_lexicon_negative(negative_word) VALUES (%s)')
            instance_model.query_sql_multiple(tuples_excel)
            flash('Berhasil import file!')
            return None
        flash('Format file tidak sesuai! Harus berekstensi .xls atau .xlsx')
        return None

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
