function infopad_init()
{
	var infopad=new $.logHandle('info','user-tools',{
		'position':'fixed',
		'top':'5px',
		'left':'40%',
		'color':'black',
		'z-index':100000
	});

	var info_fin=function(){
		infopad.hide();
	}

	var time_handle=false;
	var give_message=function(text){
		if (time_handle)
		{
			clearTimeout(time_handle);
			time_handle=false;
		}
		infopad.text(text);
		infopad.show();
		time_handle=setTimeout(info_fin,4000);
	}

	return give_message;
}
