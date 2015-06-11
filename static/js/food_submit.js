$(document).ready(function(){
	var give_message=infopad_init();

	$('form.order').live('submit',function(){
		var $this=$(this);
		var val=$this.children('input[name=amount]').val();
		var regex=new RegExp('^\\d{1,3}$');
		if (!regex.test(val)||parseInt(val)==0)
		{
			give_message('请输入正确数量');
			$this.children('input[name=amount]').focus();
			return false;
		}
		$.post($this.attr('action'),$this.serialize(),function(data){
			if (parseInt(data)==0) give_message('已加入购物车');
		});
		return false;
	});
});
