/*
 * info pad - jQuery plugin for showing a infomation area
 *
 * Copyright (c) 2010-2011 AcSco
 *
 * Licensed under the MIT license:
 *   http://www.opensource.org/licenses/mit-license.php
 *
 *
 * Version:  1.0 beta
 *
 *
 * A brief introduction for use:
	
	var handle=new $.logHandle('id','parentId');
	handle.text('HelloWorld');
 *
 * And this will show a yellow pad with the string 'HelloWorld' in the element which has the id 'parentId';
 * besides the .text() method, this Object has the following methods:
	.show():show the infoPad
	.hide():hide the infoPad
	.remove():remove the infoPad from HTML document
 *
 *
 *
 */
(function($){
	$.logHandle=function(idin,parentIdin,css)
	{
		var id=idin;
		var parentId=parentIdin;
		id=id.replace(/^#/,'');
		parentId=parentId.replace(/^#/,'');
		
		this.text=function(str){
			if (str.length==0) str='null';
		
			//如果显示区已存在，则直接替换内容
			if ($('#'+id).length>0)
			{
				$('#'+id).text(str)
					.show();
				return;
			}
			
			//主显示区
			var $info=$('<p></p>')
				.attr('id',id)
				.html(str)
				.css({
					'padding':'0px 10px 0px 10px',
					'fontWeight':'bold',
					'fontSize':'14px',
					'margin':'0',
					'text-align':'center',
					'display':'block'
				});
				
			//主显示区包装
			var $infoPad=$('<div></div>')
				.css({
					'backgroundColor':'#FFF1A8',
					'position':'relative',
				})
				.append($info)
				
			//上边框 圆角效果
			var $topBorder=$('<div></div>')
				.css({
					'border-top-color': '#FFF1A8',
					'border-bottom': '3px solid #FFF1A8',
					'border-left': '3px dotted transparent',
					'border-right': '3px dotted transparent'
				});
			
			//下边框 圆角效果
			var $buttomBorder=$('<div></div>')
				.css({
					'border-top-color': '#FFF1A8',
					'border-top': '3px solid #FFF1A8',
					'border-left': '3px dotted transparent',
					'border-right': '3px dotted transparent'
				});
			
			//总包装
			if (typeof(css)=='undefined')
			{
				css={};
			}
			$('<div></div>')
				.css('display','inline-block')
				.append($topBorder)
				.append($infoPad)
				.append($buttomBorder)
				.appendTo('#'+parentId)
				.css(css);
		}
		
		this.show=function(){
			$('#'+id).parent().parent().show();
		}
		
		this.hide=function(){
			$('#'+id).parent().parent().hide();
		}
		
		this.remove=function(){
			$('#'+id).parent().parent().remove();
		}
	}
})(jQuery);
