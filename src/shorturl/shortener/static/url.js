// Copy URL

function copyURL(e){
    myElem = $("#"+e.target.id)
    myId = myElem.data("id")
    var copyText = $("#shortURL-"+myId).text()
    navigator.clipboard.writeText(copyText);
    $("#liveToast").toast("show");
}


// Delete URL

function deleteURL(){
    urlId = $("#URLToDelete").attr("data-urlid");
    $.ajax({
        url: urlDeleteAjax,
        type: 'post',
        data: {
	    'id': urlId,
	    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
	},
        success: function(response){
	    showAlert(response.success)
	    myTable.updateTable();
            $('#deleteURLModal').modal('hide'); 
        },
	error: function(response){
	    $('#delete_url_alerts').html(response.responseJSON.error);
	    $('#delete_url_alerts').addClass("alert alert-danger");
	}
    });
}

function showModalDeleteURL(e) {
    let myElem = $("#"+e.target.id)
    var urlId = myElem.data('id');
    var urlTxt = myElem.data('txt');
    $("#URLToDelete").html(urlTxt);
    $("#URLToDelete").attr("data-urlid", urlId);
}


// URL Stats

$(document).on("click", ".showURLStatsButton", function () {
    var urlId = $(this).data('id');
    var urlTxt = $(this).data('txt');
    $.ajax({
        url: urlStatsAjax,
        type: 'post',
        data: {
	    'id': urlId,
	    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
	},
        success: function(response){
	    var urlAdded = response.dateAdded;
	    var urlTimesVisited = response.timesVisited;
	    $("#URLStatsTxt").html(urlTxt);
	    $("#URLStatsDateAdded").html(urlAdded);
	    $("#URLStatsTimesVisited").html(urlTimesVisited);
        },
	error: function(response){
	    $('#stats_url_alerts').html(response.responseJSON.error);
	    $('#stats_url_alerts').addClass("alert alert-danger");
	}
    });
});



// Add URL

$(document).ready(function(){
    
    // Evitamos que se recargue la pagina
    $("#addURLForm").submit(function(e){
        e.preventDefault();
    });
    
    // Configuramos el envio por AJAX.
    // Tener en cuenta que hay que copiar el token CSRF.
    $('#addURLSubmit').click(function(e){
        $.ajax({
            url: urlAddAjax,
            type: 'post',
            data: {
		'original': $("#id_original").val(),
		'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
	    },
            success: function(response){
		showAlert(response.success)
		myTable.updateTable();
                $('#addURLModal').modal('hide'); 
            },
	    error: function(response){
		msg = ""
		for (let anError in response.responseJSON.error) {
		    msg += response.responseJSON.error[anError]
		}
		$('#add_url_alerts').html(msg);
		$('#add_url_alerts').addClass("alert alert-danger");
	    }
        });
    });
});



// Clean all modals

$(document).ready(function(){
    // Cuando el modal se cierra, se borran los datos, las clases y mensajes.
    $('#addURLModal').on('hidden.bs.modal', function () {
	$("#id_original").val('');	  
	$('#add_url_alerts').html('');
	$('#add_url_alerts').removeClass();
    });
    
    // Cuando el modal se cierra, se borran los datos, las clases y mensajes.
    $('#deleteURLModal').on('hidden.bs.modal', function () {
	$("#URLToDelete").attr("data-urlid", "");
	$("#URLToDelete").html("");
	$('#delete_url_alerts').html('');
	$('#delete_url_alerts').removeClass();
    });
    
    // Cuando el modal se cierra, se borran los datos, las clases y mensajes.
    $('#statsURLModal').on('hidden.bs.modal', function () {
	$("#URLStatsTxt").html("");
	$("#URLStatsDateAdded").html("");
	$("#URLStatsTimesVisited").html("");
	$('#stats_url_alerts').html('');
	$('#stats_url_alerts').removeClass();
    });
})
