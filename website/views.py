import json
from flask import Blueprint, jsonify, render_template, request, flash, redirect, url_for
from website.controllers.crawling import CrawlingController

from website.controllers.dashboard import DashboardController
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

# CRAWLING
controller_crawling = CrawlingController()

@views.route('/crawling', methods=['GET'])
def crawling():
    data_crawling = controller_crawling.select_data_crawling()
    return render_template("crawling.html", data=data_crawling)

@views.route('/import-crawling', methods=['POST'])
def import_crawling():
    controller_crawling.import_crawlingExcel()
    return redirect(url_for('crawling'))


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

@views.route('/list_data_with_label', methods=['GET'])
def list_data_with_label():
    data_with_label = controller_labeling.select_dataWithLabel()
    return { 'data' : data_with_label }

@views.route('/list_data_no_label', methods=['GET'])
def list_data_no_label():
    data_no_label = controller_labeling.select_dataNoLabel()
    return { 'data' : data_no_label }


# SPLITTING DATA
controller_splitting = SplittingController()

@views.route('/splitting', methods=['GET'])
def splitting():
    return render_template('splitting.html')