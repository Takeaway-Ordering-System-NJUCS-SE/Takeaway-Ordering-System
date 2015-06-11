$(document).ready(function(){
	var $div=0;

	$('#account_change').click(function(){
		if ($div) $div.toggle();
		else
		{
			$div=$('<div></div>').appendTo('#user-tools');
			$div.load('/ajax/account_change/',function(){
				var $next=$('<input />').attr({
					'name':'next',
					'type':'hidden',
					'value':document.location.pathname,
				});

				$('#ajax_load_form')
					.append($next)
					//.append('<input type="reset" value="reset" />')
					.append('<input type="submit" value="submit" class="default" />')
					.attr('action','/accounts/login/');
			});
			$div.css({
				'position':'absolute',
				'top':'40px',
				'left':'30%',
				'padding':'2px 5px 2px 5px',
				'background':'#EFEFEF',
				'z-index':10000,
				'border':'1px solid grey',
			});
		}
		return false;
	});
});
