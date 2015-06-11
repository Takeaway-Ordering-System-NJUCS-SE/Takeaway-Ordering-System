$(document).ready(function(){
	$("span.orderwrap").click(function(){

		$(this).parent("div").siblings("div.order-list").slideToggle();
		if ($(this).text() == "Close Order")
			$(this).text("Show Order");
		else
			$(this).text("Close Order");
	});

	$("span.addwrap").click(function(){
		$(this).siblings("div.address-list").slideToggle();
		/*
		if ($(this).text() == "Show Other Addresses")
			$(this).text("Close Address");
		else
			$(this).text("Show Other Addresses");
			*/
	});

	$("div.addrs").click(function(){
		var addr = $(this).children("div.addr").text();
		var tel = $(this).children("div.tel").text();
		var name = $(this).children("div.name").text();
		var $block = $(this).parent().siblings("p");
		$block.eq(0).children("input").val(name);
		$block.eq(1).children("input").val(tel);
		$block.eq(2).children("input").val(addr);


	});
});
