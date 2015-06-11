$(document).ready(function(){
	var $submit=$('input.default');
	$submit.parents('form').submit(function(){
		$submit.val('Submitting, please wait...');
		$submit.attr('disabled','disabled');
		return true;
	});
//
//	var infopad=new $.logHandle('inf','page',{
//		'position':'fixed',
//		'top':'5px',
//		'left':'40%'
//	});
//	infopad.text('dajiahao');
//	infopad.show();
//
//	var info_fin=function(){
//		infopad.remove();
//	}
//
//	setTimeout(info_fin,2000);
});

$(document).ready(function(){
	var $id_image=$('#id_image');
	var $a=$id_image.siblings('a');
	if ($a.length>0)
	{
		var user_pic=$('<div></div>').attr('id','user_pic');
		$('<img />')
			.attr('src',$a.attr('href'))
			.after('<br />')
			.appendTo(user_pic);

		user_pic.insertAfter($id_image.siblings('br'));
	}
});
