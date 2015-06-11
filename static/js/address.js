$(document).ready(function(){
	var color_table=function(){
		$('div.address_field').removeClass('highlightBlue highlightDark');
		$('div.address_field:nth-child(odd)').addClass('highlightBlue');
		$('div.address_field:nth-child(even)').addClass('highlightDark');
	}

	color_table();

	$('div.address_field').hover(function(){
		$(this).children('div.delete').show();
	},function(){
		$(this).children('div.delete').hide();
	});

	$('div.delete a.del').live('click',function(){
		$(this).text('deleting').attr('disabled','disabled');

		var $this=$(this);
			
		$.get($(this).attr('href'),function(data){
			$this.parent().parent().remove();
			$('#full_warning').remove();
			color_table();
		});
		return false;
	});
});
