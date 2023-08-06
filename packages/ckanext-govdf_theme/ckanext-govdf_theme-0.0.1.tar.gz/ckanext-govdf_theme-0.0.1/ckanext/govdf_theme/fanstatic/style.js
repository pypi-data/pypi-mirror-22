jQuery(function($){
	$('#header-search-trigger').click(function(){
		$('#header-search-input').toggleClass('search-input-open');
		$('.head-area-busca').toggleClass('head-area-busca-open');
	});

	$(document).click(function(e){
		if(!$(e.target).closest('.ngen-search-form').length){
			$('#header-search-input').removeClass('search-input-open');
			$('.head-area-busca').removeClass('head-area-busca-open');
		}
	});

	$('#perguntas a').click(function(){
		if($('#perguntas a').hasClass('collapsed')){
	    	$('#perguntas a.collapsed').prev().prev().removeClass('panel-heading-active');
	    }
	    else{
	    	$('#perguntas a').prev().prev().addClass('panel-heading-active');
	    }
	});

	$( document ).ready(function() {
	    $('.group-item-conainter').first().removeClass('col-md-3').addClass('col-md-6');
	    $('.collapse').collapse();
	});
});