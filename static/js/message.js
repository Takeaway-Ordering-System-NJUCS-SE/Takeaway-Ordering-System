$(document).ready(function(){
	$('div.delete a').live('click',function(){
		var $this=$(this)
		$.get($this.attr('href'),function(data){
			if (data=='0') $this.parent().parent().parent().remove();
			window.location=document.location
		});
		return false;
	});
});
