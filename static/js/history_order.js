$(document).ready(function(){
	$("span.wrap").click(function(){
		$(this).siblings("div.order_item").toggle();
		if ($(this).text() == "Hide Detail")
			$(this).text("Show Detail");
		else
			$(this).text("Hide Detail");
	});


	var update=function(id){
		url = "/order/dup/"+id+"/";
		$.get(url);
	};
	$("span.add").click(function(){
		//alert($(this).siblings("span.idinfo").text());
		var $st = $(this).siblings("span.idinfo").text();
		update($st.slice(6));
	});
});
