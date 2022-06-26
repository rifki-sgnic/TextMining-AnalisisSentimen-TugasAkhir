let btn_menu = document.querySelector("#btn-menu");
let sidebar = document.querySelector(".sidebar");

btn_menu.onclick = function () {
  sidebar.classList.toggle("active");
};

// Data Table
$(document).ready(function () {
  $("#table_dataCrawling").DataTable();
  $("#table_dataPredict").DataTable();
});

// Mencari rasio data tes dan data latih
function cariRasio(kode) {
  $("#validasi_rasio").addClass("d-none");
  var jumlah_data = $("#jumlah_dataWithLabel").html();
  var rasio_hasil_test = 0;
  var rasio_hasil_train = 0;

  if (kode == "2:8") {
    // 2:8
    rasio_hasil_test = Math.floor(jumlah_data * 0.2);
    rasio_hasil_train = Math.ceil(jumlah_data * 0.8);
    $("#rasio1-hasil").html(
      '<i class="fa fa-arrow-right mr-3"></i>' +
        rasio_hasil_test +
        " Data Uji & " +
        rasio_hasil_train +
        " Data Latih"
    );
    $("#rasio2-hasil").empty();
  } else if (kode == "1:9") {
    // 1:9
    rasio_hasil_test = Math.floor(jumlah_data * 0.1);
    rasio_hasil_train = Math.ceil(jumlah_data * 0.9);
    $("#rasio1-hasil").empty();
    $("#rasio2-hasil").html(
      '<i class="fa fa-arrow-right mr-3"></i>' +
        rasio_hasil_test +
        " Data Uji & " +
        rasio_hasil_train +
        " Data Latih"
    );
  }
}

var jumlah_data_crawling = $('#countDataCrawling').html();
var jumlah_data_preprocess = $('#countDataPreprocess').html()
var jumlah_data_with_label = $('#countDataLabel').html();
var jumlah_data_train = $('#countDataTrain').html();
var jumlah_data_test = $('#countDataTest').html();
var jumlah_data_positif = $('#countDataLabelPos').html();
var jumlah_data_negatif = $('#countDataLabelNeg').html();
var jumlah_data_slangword = $('#countDataSlangword').html();
var jumlah_data_stopword = $('#countDataStopword').html();

const ctx = document.getElementById('myChart');
const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Crawling', 'Preprocess', 'Label', 'Slangword', 'Stopword'],
        datasets: [{
            label: 'Data',
            data: [
              jumlah_data_crawling, 
              jumlah_data_preprocess, 
              jumlah_data_with_label, 
              jumlah_data_slangword, 
              jumlah_data_stopword
            ],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

const ctxSplit = document.getElementById('chart-split-data').getContext('2d');
const chartSplit = new Chart(ctxSplit, {
    type: 'doughnut',
    data: {
      labels: [
        'Train',
        'Test'
      ],
      datasets: [{
        label: 'Pembagian Data',
        data: [jumlah_data_train, jumlah_data_test],
        backgroundColor: [
          'rgb(54, 162, 235)',
          'rgb(255, 99, 132)'
        ],
        hoverOffset: 4
      }]
    }
});