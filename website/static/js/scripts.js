let btn_menu = document.querySelector("#btn-menu");
let sidebar = document.querySelector(".sidebar");

btn_menu.onclick = function() {
    sidebar.classList.toggle("active");
}

const charts = document.querySelectorAll(".chart");

charts.forEach(function (chart) {
    var ctx = chart.getContext("2d");
    var myChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: ["Data Latih", "Data Uji"],
        datasets: [
          {
            label: "# of Data",
            data: [802, 201],
            backgroundColor: [
              "rgba(255, 99, 132, 0.2)",
              "rgba(54, 162, 235, 0.2)",
            ],
            borderColor: [
              "rgba(255, 99, 132, 1)",
              "rgba(54, 162, 235, 1)",
            ],
            borderWidth: 1,
          },
        ],
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
});

// validasi untuk tanggal pengambilan crawling awal
var min = new Date();
min.setDate(min.getDate()-7);
$('#tanggal_awal').attr('min', getHtmlDateString(min));
$('#tanggal_akhir').attr('min', getHtmlDateString(min));
$('#tanggal_awal').on("change paste keyup", function() {
	$('#tanggal_akhir').attr('min', $('#tanggal_awal').val());

	var date1 = new Date($(this).val());
	var date2 = new Date($('#tanggal_akhir').val());
	if(date1 > date2) {
		$('#tanggal_akhir').val($('#tanggal_awal').val());
	}
});

// validasi untuk tanggal pengambilan crawling akhir
var max = new Date();
max.setDate(max.getDate());
$('#tanggal_awal').attr('max', getHtmlDateString(max));
$('#tanggal_akhir').attr('max', getHtmlDateString(max));

// generate tanggal(yyy-mm-dd) berdasarkan parameter instance date
function getHtmlDateString(date) {
	var dd = date.getDate();
	var mm = date.getMonth()+1;
	var yyyy = date.getFullYear();
	if(dd<10){
		dd = '0'+dd;
	} 
	if(mm<10){
		mm = '0'+mm;
	}
	return yyyy+'-'+mm+'-'+dd;
}

// Data Table
$(document).ready(function () {
    $('#table_dataCrawling').DataTable();
});