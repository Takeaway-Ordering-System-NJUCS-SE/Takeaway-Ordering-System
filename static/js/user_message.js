$(document).ready(function(){
	var text=$('#user_message li').eq(0).text();
	if (typeof(text)=='undefined') return;

	var infopad=new $.logHandle('inf','user-tools',{
		'position':'fixed',
		'top':'5px',
		'left':'40%',
		'color':'black'
	});

	infopad.text(text);
	infopad.show();

	var info_fin=function(){
		infopad.remove();
	}

	setTimeout(info_fin,4000);
});
