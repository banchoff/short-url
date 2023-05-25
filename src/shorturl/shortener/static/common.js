function showAlert(msg){
    div = '<div class="alert alert-success alert-dismissible fade show" role="alert">'
    div += msg
    div += '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>'
    $('#alertsContainer').html(div)
}
