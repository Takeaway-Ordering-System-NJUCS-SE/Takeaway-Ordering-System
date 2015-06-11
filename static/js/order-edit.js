$(document).ready(function(){
	var recal=function(){
		var total=0;
		$("div.money").each(function(){
			var c = $(this).children("span").text();
			var a = $(this).children("input").val();
			total += parseFloat(c) * parseInt(a);
		});
		$("span.total").text(total);
	};

	var update=function(id, amount){
		url = "/order/update/"+id+"/";
		amount = parseInt(amount);
		$.get(url, {"amount":amount});
	};

	$('p.Delete').click(function()
	{
	//	alert ($(this).next().text());
		$(this).parent().parent().hide();
		var input=$(this).next("div.money").children("input");
		input.val('0');
		var $count=$("span.count");
		$count.text(parseInt($count.text())-1);
		
		recal();
		update(input.attr('name'), input.val());
	});

	$('input').change(function()
	{
		if (isNaN($(this).val()))
			$(this).val('1');
		
		if ($(this).val()[0] == '-')
			$(this).val('0');
	
		recal();
		update($(this).attr('name'), $(this).val());
	});

	$('input#discard').click(function(){
		var btn = confirm("删除订单？");
		if (btn == false)
			return false;
	});


});
