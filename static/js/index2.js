$(document).ready(function(){
	var totsib = $("span.nav");
	var totdiv = $("div.order");

	totsib.live('click',function(){
		totsib.addClass("inv").removeClass("vis");
		$(this).removeClass("inv").addClass("vis");

		var cls=$(this).attr("id");
		$div = $("#div"+cls);
		totdiv.addClass("inv");
		$div.removeClass("inv");
	});
});
