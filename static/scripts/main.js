// <refrence path="jQuery-1.9.1.min.js" />
(function($){
	$.fn.bScrollAnimate = function(options){
        var options = {
            classToAdd: 'animated',
            offset: 100,
            callbackFunction: function(elem){}
        };
        $.extend(options, options);
        var $elem = this,
            windowHeight = $(window).height();
        this.checkViewportElm = function(){
            var scrollElem = ((navigator.userAgent.toLowerCase().indexOf('webkit') != -1) ? 'body' : 'html'),
                viewportTop = $(scrollElem).scrollTop(),
                viewportBottom = (viewportTop + windowHeight);
            $(document).find($elem).each(function(){
                var $obj = $(this);
                if ($obj.hasClass(options.classToAdd)){
                    return;
                }
                var elemTop = Math.round( $obj.offset().top ) + options.offset,
                    elemBottom = elemTop + ($obj.height());
                if ((elemTop < viewportBottom) && (elemBottom > viewportTop)){
                    $obj.addClass(options.classToAdd);
                    options.callbackFunction($obj);
                }
            });
        };
        $(document).scroll(this.checkViewportElm);
        this.checkViewportElm();
        $(window).resize(function(e){
            windowHeight = e.currentTarget.innerHeight;
        });
    };
})(jQuery);
$(function(){
	$('.menu.landingPage li > a[href*=#]:not([href=#])').bind('click dblclick ontouchstart', function() {
    	if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
      		var target = $(this.hash);
      		target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
  			if (target.length) {
  				// $('.menu li').removeClass('onvisible');
  				// $(this).parent('li').addClass('onvisible');
        		$('html,body').stop().animate({
          			scrollTop: target.offset().top - 60
        		}, 1000);
        		$('.section').removeClass('isvisible');	
        		$('.section#'+this.hash.replace('#', '')).addClass('isvisible');
        		window.location.hash = this.hash;
        		if($('.menu').hasClass('visible')){
        			$('.menu.visible').removeClass('visible');
        		}
        		return false;
      		}
		}
  	});
});

$(document).ready(function(e){
	$(document).find('.run').addClass("hidden-elm").bScrollAnimate({
    	classToAdd: 'animated',
    	offset: 100    
   	});
   	$('#remaining').countdown({
        // date = 12 bahman 94 9:00 AM
        // TODO: get time from server
		date: '03/02/2016 07:29:59',
		offset: -8,
		day: 'روز',
		days: 'روز'
	}, function () {
		var text = '';
		if($('body').hasClass('ltr')){
			text = 'Challenge has been finished';
		}else{
			text = 'مسابقه‌ی نهایی پایان یافت';
		}
		$('.notify').html(text);
	});

	$('.btn--top').on('click', function(e){
		e.preventDefault();
		$('html, body').animate({scrollTop: 0}, 555);
	});

	$('.mobile').on('click', '.menu-button', function(e){
		e.preventDefault();
		e.stopPropagation();
		$(this).parent().find('.menu').toggleClass('visible');
	});
	$(document).on('click', function(){
		$('.menu.visible').removeClass('visible');
	});
});
// و الحمد الله رب العالمین