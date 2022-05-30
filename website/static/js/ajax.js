/**
 *  AJAX CRAWLING
 */

// TODO

/**
 *  AJAX PREPROCESSING
 */
// TAMPIL DATA PREPROCESSING [START]
var table_dataPreprocessing = $('#table_dataPreprocessing').DataTable({
	"deferRender": true,
	"ajax": "/list-data-preprocessing",
	"columns": [
		{
			data: null, 
			"render": function (data, type, full, meta) {
				return  meta.row + 1;
			}
		},
		{
			data: null,
			"render": function(data, type, full, meta) {
				return BigInt(data.id).toString();
			}
		},
		{
			data: null,
			className: 'text-left',
			"render": function (data, type, full, meta) {
				return data.clean_text +'<br /><button type="button" value="modalTweetAsli" class="btn btn-primary btn-sm float-right mt-2"><i class="bx bx-search"></i> Lihat Tweet Asli</button>'
			},
		},
		{ data: 'user' },
		{
			data: null,
			"render": function(data, type, full, meta) {
           		return moment(data.created_at).format("LLL");
			}
		},
	],
});

// AKSI LIHAT TWEET ASLI DENGAN MODAL
$('#table_dataPreprocessing tbody').on( 'click', 'button', function () {
	var data = table_dataPreprocessing.row($(this).parents('tr')).data();
	if($(this).prop("value") == 'modalTweetAsli') {
		$("#modalLihatTweetAsli").find("p[id='tweetAsli']").html(data['text']);
		$("#modalLihatTweetAsli").find("p[id='tweetBersih']").html(data['clean_text']);
		$('#modalLihatTweetAsli').modal('show');
	}
});
// TAMPIL DATA PREPROCESSING [END]

$('#preprocessing_data').click(function() {

	var form_dataArray = $('form').serializeArray();
	var jumlah_data_crawling = parseInt($('#jumlah_dataCrawling').html());
	
	// validasi data preprocessing
	if(jumlah_data_crawling > 0 && form_dataArray[0]['name'].trim() == 'aksi' && form_dataArray[0]['value'].trim() == 'preprocessing') {
		var content =	"";
		
		$.ajax({
			url         : "/preprocessing",
			data		: $('form').serialize(),
			type        : "POST",
			dataType	: "json",
			beforeSend  : function() {		

				content +=	`
								<div class="bs-callout bs-callout-primary mt-0">
									<h4>Data <em>Preprocessing</em></h4>
									<p class="text-muted"><em>Preprocessing</em> <strong>`+ jumlah_data_crawling +`</strong> data <em>crawling</em></p>
								</div>
								
								<div class="loaderDiv my-5 m-auto"></div>
							`;
							
				$('#content-preprocessing').html(content);
        $('body').css("overflow", "");
				$(".loaderDiv").show();
			},
			success     : function(response) {
				content +=	`
								<div class="col-md-6 offset-md-3 col-sm-12 text-center border border-success rounded shadow py-4">
									<label class="text-center d-flex justify-content-center align-items-center mb-0">
										<span class="mr-2 text-muted"> Berhasil melakukan <em>preprocessing</em>. </span>
										<div class="d-inline-flex align-items-center">
											<h3 class="text-info mb-0">`+ jumlah_data_crawling +`</h3>
											<span class="ml-2 text-muted"> Data telah disimpan!</span>
										</div>
									</label>
								</div>
								<div class="table-responsive-sm">
									<table class="table table-bordered table-striped text-center" id="myTable">
										<thead>
											<tr>
												<th>No.</th>
												<th>Teks Bersih</th>
												<th>Pilihan</th>
											</tr>
										</thead>
										<tbody>
							`;
							
				$.each(response.last_data, function(index) {
					content +=	`
											<tr>
												<td>`+ ++index +`</td>
												<td class="text-left">`+ response.last_data[--index] +`</td>
												<td class="text-center"><button class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#modalDetailPreprocessing`+ index +`"><i class="bx bx-search"></i> Detail</button></td>
											</tr>
											
											<div class="modal fade" id="modalDetailPreprocessing`+ index +`" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
												<div class="modal-dialog modal-lg">
													<div class="modal-content">
														<div class="modal-header">
															<h5 class="modal-title" id="exampleModalLabel">Detail <em>Preprocessing</em> Tweet</h5>
															<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
														</div>
														<div class="modal-body px-5">
															<div class="row">
																<div class="col-md-12 d-flex justify-content-start align-items-center">
																	<div class="timeline">
																		<p><span>1. Tweet Awal</span><br />`+ response.first_data[index] +`</p>
																		<p><span>2. Case Folding</span><br />`+ response.casefolding[index]+`</p>
																		<p><span>3. Menghapus URL, Mention, Hastag, Selain Huruf, Spasi Berlebih (<em>Cleansing</em>)</span><br />`+ response.remove_non_char[index]+`</p>
																		<p><span>4. Mengubah kata tidak baku ke bentuk kata baku (<em>Slang Word</em>)</span><br />`+ response.change_slangword[index]+`</p>
																		<p><span>5. Menghapus <em>Stop Word</em></span><br />`+ response.remove_stopword[index]+`</p>
																		<p><span>6. Mengubah kata berimbuhan ke bentuk kata dasar (<em>Stemming</em>)</span><br />`+ response.change_stemming[index]+`</p>
																	</div>
																</div>
															</div>
														</div>
													</div>
												</div>
											</div>
								`;
				});
				
				content +=	`			
                    </tbody>
								  </table>
							  </div>
							  <div class="col-md-6 offset-md-3 col-sm-12 text-center">
								  <a href="/preprocessing" class="btn btn-info w-50 text-decoration-none"><i class="fa fa-arrow-left"></i> Kembali</a>
							  </div>
						  `;
				
				$('#content-preprocessing').html(content);
				
				$(".loaderDiv").hide();
				$('#myTable').DataTable();
				
				$('#modalPreprocessing').modal('toggle');
				$('body').removeClass('modal-open');
				$('.modal-backdrop').remove();
			},
			error     : function(x) {
				console.log(x.responseText);
			}
		});
	} 
	else {
		$('#validasi_preprocessing').removeClass('d-none');
	}
});



/**
 *  AJAX LABELING
 */

// TAMPIL DATA LABELING (DENGAN LABEL) [START]
var table_dataWithLabel = $('#table_dataWithLabel').DataTable({
	"deferRender": true,
	"ajax": "/list_data_with_label",
	"columns": [
		{
			data: null, 
			"render": function (data, type, full, meta) {
				return  meta.row + 1;
			}
		},
		{
			data: null,
			"render": function(data, type, full, meta) {
				return BigInt(data.id).toString();
			}
		},
		{
			data: null,
			className: 'text-left',
			"render": function (data, type, full, meta) {
				return data.clean_text +'<br /><button type="button" value="modalTweetAsli" class="btn btn-primary btn-sm float-right mt-2"><i class="bx bx-search"></i> Lihat Tweet Asli</button>'
			},
		},
		{ data: 'user' },
		{
			data: null,
			"render": function(data, type, full, meta) {
           		return moment(data.created_at).format("LLL");
			}
		},
		{
			data: null,
			"render": function (data, type, full, meta) {
				if(data.sentiment_type == 'positif') {
					return '<label class="btn btn-success disabled">POSITIF</label>';
				}
				else if(data.sentiment_type == 'negatif') {
					return '<label class="btn btn-danger disabled">NEGATIF</label>';
				}
				return '<label class="btn btn-secondary disabled">NETRAL</label>';
			},
		},
	],
});
// AKSI LIHAT TWEET ASLI DENGAN MODAL
$('#table_dataWithLabel tbody').on( 'click', 'button', function () {
	var data = table_dataWithLabel.row($(this).parents('tr')).data();
	if($(this).prop("value") == 'modalTweetAsli') {
		$("#modalLihatTweetAsli").find("p[id='tweetAsli']").html(data['text']);
		$("#modalLihatTweetAsli").find("p[id='tweetBersih']").html(data['clean_text']);
		$('#modalLihatTweetAsli').modal('show');
	}
});
// TAMPIL DATA LABELING (DENGAN LABEL) [END]

// TAMPIL DATA LABELING (TANPA LABEL) [START]
var table_dataNoLabel = $('#table_dataNoLabel').DataTable({
	"deferRender": true,
	"ajax": "/list_data_no_label",
	"columns": [
		{
			data: null, 
			"render": function (data, type, full, meta) {
				return  meta.row + 1;
			}
		},
		{
			data: null,
			className: 'text-left',
			"render": function (data, type, full, meta) {
				return data.text +'<br /><button type="button" value="modalLihatCleanTextLabeling" class="btn btn-primary btn-sm float-right mt-2"><i class="bx bx-search"></i> Lihat Teks Bersih</button>'
			},
		},
		{
			data: null,
			"render": function () {
				return `
					<select class="custom-select" name="label_data">
						<option value="" selected disabled>Pilih</option>
						<option value="positif">Positif</option>
						<option value="negatif">Negatif</option>
					</select>
				`;
			},
		},
	],
});

// AKSI LIHAT TWEET ASLI DENGAN MODAL
$('#table_dataNoLabel tbody').on( 'click', 'button', function () {
	var data = table_dataNoLabel.row($(this).parents('tr')).data();
	if($(this).prop("value") == 'modalLihatCleanTextLabeling') {
		$("#modalLihatCleanTextLabeling").find("p[id='tweetAsliLabeling']").html(data['text']);
		$("#modalLihatCleanTextLabeling").find("p[id='tweetBersihLabeling']").html(data['clean_text']);
		$('#modalLihatCleanTextLabeling').modal('show');
		$('#modalLihatCleanTextLabeling').css('background-color', 'rgba(0,0,0,0.3)');
	}
});

// FUNGSI MENGEMBALIKAN TAMPILAN SETELAH NESTED MODAL modalLihatCleanTextLabeling DITUTUP
$('#modalLihatCleanTextLabeling').on('hidden.bs.modal', function () {
	$('body').addClass('modal-open');
});

// AJAX LABELING MANUAL
$('#table_dataNoLabel tbody').on( 'change', 'select[name="label_data"]', function () {
	var data = table_dataNoLabel.row($(this).parents('tr')).data();
	id = BigInt(data['id']).toString();
	value = $(this).find(":selected").text();
	
	$.ajax({
		url         : "/labeling",
		data		: {'id': id, 'value': value},
		type        : "POST",
		dataType	: "json",
		success     : function(response) {
			console.log(response);
		},
		error     : function(x) {
			console.log(x.responseText);
		}
	});
});
// TAMPIL DATA LABELING (TANPA LABEL) [END]

// AUTO REFRESH PAGE SETELAH PROSES PELABELAN AJAX
$('#modalLabeling').on('hidden.bs.modal', function () {
	window.location.href = "/labeling";
});


/**
 *  AJAX SPLITTING
 */

// TODO

/**
 *  AJAX MODELING
 */

// TODO

/**
 *  AJAX VALIDATION
 */

// TODO

/**
 *  AJAX EVALUATION
 */

// TODO