$(document).ready(function(){
	var give_message = infopad_init();

	$("span.food-order").live("click", function()
	{
		$this = $(this);
		var $hidden=$(this).next();
		$hidden.toggle();
		$hidden.children("form").children("input.amount").focus();
		if ($(this).next().is(':hidden')) $(this).text('添加到购物篮');
		else $(this).text('关闭');
	});

	$("div.label").live('mouseover',function(){
		var $this=$(this);
		$this.siblings("div.label").addClass("inv").removeClass("vis");
		$this.removeClass("inv").addClass("vis");

		var cls=$this.attr("id");
		$div=$("fieldset."+cls);
		$div.siblings("fieldset").addClass("inv");
		$div.removeClass("inv");
	});

	var update=function(id){
		url = "/order/dup/"+id+"/";
		$.get(url);
	};
	$("span.add").live('click',function(){
		//alert($(this).siblings("span.idinfo").text());
		var $st = $(this).parent().parent("div.recorder").attr("id");
		update($st.slice(5));
		give_message('Order Successfully');
	});
	$('form#discard').submit(function(){
		var btn=comfirm("Delete the Order?");
		if (btn == false)
			return false;
	});
});
$(document).ready(function(){
	var give_message=infopad_init();

	$('form.order').live('submit',function(){
		var $this=$(this);

		var val=$this.children('input[name=amount]').val();
		var regex=new RegExp('^\\d{1,3}$');
		if (!regex.test(val)||parseInt(val)==0)
		{
			give_message('please give a valid amount');
			$this.children('input[name=amount]').focus();
			return false;
		}

		$this.parent().siblings("span.food-order").text('添加到购物篮');
		$.post('/recommands/ajax/',$this.serialize(),function(data){
			$this.parent().hide();
			if (parseInt(data)==0) give_message('Your order have been added to your shopping cart');
		});
		return false;
	});
});
