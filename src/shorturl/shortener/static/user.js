
// Delete User

function deleteUser(){
    userId = $("#UserToDelete").attr("data-user-id");
    $.ajax({
        url: userDeleteAjax,
        type: 'post',
        data: {
	    'id': userId,
	    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
	},
        success: function(response){
	    showAlert(response.success)
	    myTable.updateTable()
            $('#deleteUserModal').modal('hide'); 
        },
	error: function(response){
	    $('#delete_user_alerts').html(response.responseJSON.error);
	    $('#delete_user_alerts').addClass("alert alert-danger");
	}
    });
}

$(document).on("click", ".deleteUserModalButton", function () {
    var userId = $(this).data('user-id');
    var userName = $(this).data('user-username');
    $("#UserToDelete").html(userName);
    $("#UserToDelete").attr("data-user-id", userId);
});



// Toggle user between admin and not admin
$(document).on("click", ".toggleUserAdminButton", function () {
    var userId = $(this).data('user-id');
    $("#toggleUserTitle").removeClass()    
    $.ajax({
        url: userToggleAjax,
        type: 'post',
        data: {
	    'id': userId,
	    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
	},
        success: function(response){
	    $("#toggleUserTitle").html("User changed")
	    $("#toggleUserTitle").addClass("toast-header bg-success-subtle text-emphasis-success")
	    msg = "User changed. Now user "
	    if (response.userState == "ADMIN") {
		msg += "is Admin"
		$("#toggleUserAdminButton-"+userId).html("Drop admin")
	    }
	    if (response.userState == "NOTADMIN") {
		msg += "is NOT Admin"
		$("#toggleUserAdminButton-"+userId).html("Make admin")
	    }
	    $("#toggleUserBody").html(msg)
	    $("#liveToast").toast("show");
        },
	error: function(response){
	    $("#toggleUserTitle").html("User NOT changed")
	    $("#toggleUserTitle").addClass("toast-header bg-danger-subtle text-emphasis-danger")
	    msg = "User NOT changed. User continues being  "
	    if (response.responseJSON.userState == "ADMIN") {
		msg += "Admin"
	    }
	    if (response.responseJSON.userState == "NOTADMIN") {
		msg += "NOT Admin"
	    }
	    msg += "<br>Error: "+response.responseJSON.error
	    $("#toggleUserBody").html(msg)
	    $("#liveToast").toast("show");
	}
    });
});

// Add User
$(document).ready(function(){
    // Evitamos que se recargue la pagina
    $("#addUserForm").submit(function(e){
        e.preventDefault();
    });
    $('#addUserSubmit').click(function(e){
        $.ajax({
            url: userAddAjax,
            type: 'post',
            data: {
		'username': $("#id_username").val(),
		'email': $("#id_email").val(),
		'password1': $("#id_password1").val(),
		'password2': $("#id_password2").val(),
		'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
	    },
            success: function(response){
		showAlert(response.success)
		myTable.updateTable()
                $('#addUserModal').modal('hide'); 
            },
	    error: function(response){
		msg = "<ul>"
		// TODO: mostrar el campo problematico junto con el error. Ej.: Username: algun error.
		for (let anError in response.responseJSON.error) {
		    for (var i = 0; i < response.responseJSON.error[anError].length; i++) {
			msg += "<li>"+anError+ ": " + response.responseJSON.error[anError][i] + "</li>"
		    }
		}
		msg += "</ul>"
		$('#add_user_alerts').html(msg);
		$('#add_user_alerts').addClass("alert alert-danger");
	    }
        });
    });
})


// Change Password
$(document).on("click", ".changePasswordModalButton", function () {
    var userId = $(this).data('user-id');
    $("#UserChangePassword").val(userId);
});

$(document).ready(function(){    
    // Evitamos que se recargue la pagina
    $("#changeUserPasswordForm").submit(function(e){
        e.preventDefault();
    });
        
    $('#changePasswordSubmit').click(function(e){
        $.ajax({
            url: userChangePWAjax,
            type: 'post',
            data: {
		'id': $("#UserChangePassword").val(),
		'password1': $("#password1").val(),
		'password2': $("#password2").val(),
		'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
	    },
            success: function(response){
		showAlert(response.success)
                $('#changePasswordUserModal').modal('hide'); 
            },
	    error: function(response){
		$('#change_password_alerts').html(response.responseJSON.error);
		$('#change_password_alerts').addClass("alert alert-danger");
	    }
        });
    });      
}); 


// Cleaning all modals when closing them
$(document).ready(function(){
    // Cuando el modal se cierra, se borran los datos, las clases y mensajes.
    $('#deleteUserModal').on('hidden.bs.modal', function () {
	$("#UserToDelete").html("");
	$('#delete_user_alerts').html('');
	$('#delete_user_alerts').removeClass();
    });      

    // Cuando el modal se cierra, se borran los datos, las clases y mensajes.
    $('#changePasswordUserModal').on('hidden.bs.modal', function () {
	$("#UserChangePassword").val("");
	$("#password1").val("");
	$("#password2").val("");
	$('#change_password_alerts').html('');
	$('#change_password_alerts').removeClass();
    });      

    // Cuando el modal se cierra, se borran los datos, las clases y mensajes.
    $('#addUserModal').on('hidden.bs.modal', function () {
	$("#id_username").val('');  
	$("#id_email").val('');  
	$("#id_password1").val('');
	$("#id_password2").val('');
	$('#add_user_alerts').html('');
	$('#add_user_alerts').removeClass();
    });
})
