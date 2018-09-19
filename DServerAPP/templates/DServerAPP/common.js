function bAlert(bId, msg) {
	var content = '<div class="alert alert-danger alert-dismissible" role="alert">'+
						  	'<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'+
							  '<span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span>'+
							  '<span class="sr-only">Error:</span>'+
							  msg+
							'</div>';
	$('#'+bId).parent().after(content);
}