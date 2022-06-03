import json
from flask import Blueprint, jsonify, render_template, request, flash, redirect, url_for
from website.controllers.crawling import CrawlingController

from website.controllers.dashboard import DashboardController
from website.controllers.kamus import KamusController
from website.controllers.labeling import LabelingController
from website.controllers.preprocessing import PreprocessingController
from website.controllers.splitting import SplittingController

views = Blueprint('views', __name__)

# DASHBOARD

controller_dashboard = DashboardController()
@views.route('/', methods=['GET'])
def dashboard():
    data = controller_dashboard.getData()
    return render_template("dashboard.html", data=data)

# KAMUS
controller_kamus = KamusController()
@views.route('/kamus', methods=['GET'])
def kamus():
    return render_template("kamus.html")

## Positif
@views.route('/kamus/list-kata-positif', methods=['GET'])
def list_kata_positif():
    data_positif = controller_kamus.select_dataKataPositif()
    return { 'data' : data_positif }

@views.route('/kamus/kata-positif/tambah', methods=['POST'])
def tambah_kata_positif():
    controller_kamus.add_dataKataPositif()
    return redirect(url_for('views.kamus'))

@views.route('/kamus/kata-positif/import', methods=['POST'])
def import_kata_positif():
    controller_kamus.import_dataKataPositif()
    return redirect(url_for('views.kamus'))

@views.route('/kamus/kata-positif/ubah', methods=['POST'])
def ubah_kata_positif():
    controller_kamus.update_dataKataPositif()
    return redirect(url_for('views.kamus'))

@views.route('/kamus/kata-positif/hapus', methods=['POST'])
def hapus_kata_positif():
    controller_kamus.delete_dataKataPositif()
    return redirect(url_for('views.kamus'))

@views.route('/kamus/kata-positif/hapus-all', methods=['POST'])
def hapus_all_kata_positif():
    controller_kamus.delete_allDataKataPositif()
    return redirect(url_for('views.kamus'))

## Negatif
@views.route('/kamus/list-kata-negatif')
def list_kata_negatif():
    data_negatif = controller_kamus.select_dataKataNegatif()
    return { 'data' : data_negatif }

@views.route('/kamus/kata-negatif/tambah', methods=['POST'])
def tambah_kata_negatif():
    controller_kamus.add_dataKataNegatif()
    return redirect(url_for('views.kamus'))

@views.route('/kamus/kata-negatif/import', methods=['POST'])
def import_data_kata_negatif():
    controller_kamus.import_dataKataNegatif()
    return redirect(url_for('views.kamus'))

@views.route('/kamus/kata-negatif/ubah', methods=['POST'])
def ubah_kata_negatif():
    controller_kamus.update_dataKataNegatif()
    return redirect(url_for('views.kamus'))

@views.route('/kamus/kata-negatif/hapus', methods=['POST'])
def hapus_kata_negatif():
    controller_kamus.delete_dataKataNegatif()
    return redirect(url_for('views.kamus'))

@views.route('/kamus/kata-negatif/hapus-all', methods=['POST'])
def hapus_all_kata_negatif():
    controller_kamus.delete_allDataKataNegatif()
    return redirect(url_for('views.kamus'))

## Slangword
@views.route('/kamus/list-slangword', methods=['GET'])
def list_slangword():
    slangword = controller_kamus.select_dataSlangword()
    return { 'data' : slangword }

@views.route('/kamus/slangword/tambah', methods=['POST'])
def tambah_slangword():
    controller_kamus.add_dataSlangword()
    return redirect(url_for('views.kamus'))

@views.route('/kamus/slangword/import', methods=['POST'])
def import_data_slangword():
    controller_kamus.import_dataSlangword()
    return redirect(url_for('views.kamus'))

@views.route('/kamus/slangword/ubah', methods=['POST'])
def ubah_slangword():
    controller_kamus.update_dataSlangword()
    return redirect(url_for('views.kamus'))

@views.route('/kamus/slangword/hapus', methods=['POST'])
def hapus_slangword():
    controller_kamus.delete_dataSlangword()
    return redirect(url_for('views.kamus'))

@views.route('/kamus/slangword/hapus-all', methods=['POST'])
def hapus_all_slangword():
    controller_kamus.delete_allDataSlangword()
    return redirect(url_for('views.kamus'))

# Stopword
@views.route('/kamus/list-stopword', methods=['GET'])
def list_stopword():
    stopword = controller_kamus.select_dataStopword()
    return { 'data' : stopword }

@views.route('/kamus/stopword/tambah', methods=['POST'])
def tambah_stopword():
    controller_kamus.add_dataStopword()
    return redirect(url_for('views.kamus'))

@views.route('/kamus/stopword/import', methods=['POST'])
def import_data_stopword():
    controller_kamus.import_dataStopword()
    return redirect(url_for('views.kamus'))

@views.route('/kamus/stopword/ubah', methods=['POST'])
def ubah_stopword():
    controller_kamus.update_dataStopword()
    return redirect(url_for('views.kamus'))

@views.route('/kamus/stopword/hapus', methods=['POST'])
def hapus_stopword():
    controller_kamus.delete_dataStopword()
    return redirect(url_for('views.kamus'))

@views.route('/kamus/stopword/hapus-all', methods=['POST'])
def hapus_all_stopword():
    controller_kamus.delete_allDataStopword()
    return redirect(url_for('views.kamus'))


# CRAWLING
controller_crawling = CrawlingController()

@views.route('/crawling', methods=['GET'])
def crawling():
    data_crawling = controller_crawling.select_data_crawling()
    return render_template("crawling.html", data=data_crawling)

@views.route('/import-crawling', methods=['POST'])
def import_crawling():
    controller_crawling.import_crawlingExcel()
    return redirect(url_for('views.crawling'))


# PREPROCESSING
controller_preprocessing = PreprocessingController()

@views.route('/preprocessing', methods=['GET','POST'])
def preprocessing():
    if request.method == 'GET':
        count_data_crawling = controller_preprocessing.count_dataCrawling()
        return render_template("preprocessing.html", count_data_crawling=count_data_crawling)

    if request.method == 'POST':
        response = controller_preprocessing.add_dataPreprocessing()
        return response

@views.route('/list-data-preprocessing', methods=['GET'])
def list_data_preprocessing():
    data_preprocessing = controller_preprocessing.select_dataPreprocessing()
    return { 'data' : data_preprocessing }

# LABELING
controller_labeling = LabelingController()

@views.route('/labeling', methods=['GET','POST'])
def labeling():
    if request.method == 'GET':
        count_data_with_label = controller_labeling.count_dataWithLabel()
        return render_template("labeling.html", count_data_with_label=count_data_with_label)
    
    if request.method == 'POST':
        response = controller_labeling.add_dataLabeling()
        return response

@views.route('/list-data-with-label', methods=['GET'])
def list_data_with_label():
    data_with_label = controller_labeling.select_dataWithLabel()
    return { 'data' : data_with_label }

@views.route('/list-data-no-label', methods=['GET'])
def list_data_no_label():
    data_no_label = controller_labeling.select_dataNoLabel()
    return { 'data' : data_no_label }


# SPLITTING DATA
controller_splitting = SplittingController()

@views.route('/split', methods=['GET', 'POST'])
def split():
    if request.method == 'GET':
        count_data_with_label = controller_splitting.count_dataWithLabel()
        return render_template('splitting.html', count_data_with_label=count_data_with_label)
    
    if request.method == 'POST':
        response = controller_splitting.add_dataSplit()
        return response

@views.route('/split/list-data-train', methods=['GET'])
def list_data_train():
    data_train = controller_splitting.select_dataTrain()
    return { 'data' : data_train }

@views.route('/split/list-data-test', methods=['GET'])
def list_data_test():
    data_test = controller_splitting.select_dataTest()
    return { 'data' : data_test }

@views.route('/split/hapus', methods=['POST'])
def hapus_dataSplit():
    controller_splitting.delete_allDataSplit()
    return redirect(url_for('views.split'))
