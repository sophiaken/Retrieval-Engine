// JavaScript Document
$(function() {
	 "use strict";
  var topoffset = 50; //variable for menu height
  
    //Activate Scrollspy
  $('body').scrollspy({
    target: '.navbar-fixed-top',
    offset: topoffset
  });

 // Add an inbody class to nav when scrollspy event fires
  $('.navbar-fixed-top').on('activate.bs.scrollspy', function() {
    var hash = $(this).find('li.active a').attr('href');
    if(hash !== '#carousel1') {
	  if(! $('nav.navbar').hasClass('inbody')){
   		   $('nav.navbar').velocity('transition.slideDownIn');
	  }
      $('nav.navbar').addClass('inbody');
    } else {
	    $('nav.navbar').removeClass('inbody');
	    $('nav.navbar').velocity('transition.slideUpIn');
    }
  });
 
//Use smooth scrolling when clicking on navigation
  $('.navbar a[href*=#]:not([href=#]),.carousel-caption a[href*=#features],.totop').click(function() {
    if (location.pathname.replace(/^\//,'') === 
      this.pathname.replace(/^\//,'') && 
      location.hostname === this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if (target.length) {
        $('html,body').animate({
          scrollTop: target.offset().top-topoffset+2
        }, 500);
        return false;
      } //target.length
    } //click function
  }); //smooth scrolling

  // sections animations

  $('nav.navbar-fixed-top').velocity('transition.flipBounceYIn'); 
  $("#blog,#features,#portfolio,#about,#contact,#testimonials,.carousel-indicators,.carousel-control").velocity({ opacity: 0 });

  var ctrl = new ScrollMagic.Controller({
        globalSceneOptions: {
            triggerHook: 'onCenter'
        }
    });

    var scene2 = new ScrollMagic.Scene({triggerElement: '#features'}).setVelocity('#features',{opacity:1}).setVelocity('#features','transition.slideUpBigIn').addTo(ctrl);
    var scene  = new ScrollMagic.Scene({triggerElement: '#blog'}).setVelocity('#blog',{opacity:1}).setVelocity('#blog','transition.slideLeftIn').addTo(ctrl);
    var scene3 = new ScrollMagic.Scene({triggerElement: '#portfolio'}).setVelocity('#portfolio',{opacity:1}).setVelocity('#portfolio','transition.slideRightIn').addTo(ctrl);
    var scene4 = new ScrollMagic.Scene({triggerElement: '#testimonials'}).setVelocity('#testimonials',{opacity:1}).setVelocity('#testimonials','transition.fadeIn').addTo(ctrl);
    var scene5 = new ScrollMagic.Scene({triggerElement: '#about'}).setVelocity('#about',{opacity:1}).setVelocity('#about','transition.slideDownBigIn',function(){$('#about .inner').countTo({formatter: function(value, options) {
                var skill = $(this).data('skill');
		    var counted = value.toFixed(options.decimal);
		    $(this).text( skill + ':  ' + counted + '%').css({"width":counted + "%"});
      }});}).addTo(ctrl);
    var scene6 = new ScrollMagic.Scene({triggerElement: '#contact'}).setVelocity('#contact',{opacity:1}).setVelocity('#contact','transition.slideUpBigIn').addTo(ctrl);
  
  	// spicing up the carousel
      $(".carousel-caption h3,.carousel-caption p,.carousel-caption > a").velocity({ opacity: 0 });

	$('.carousel-caption h3').velocity('transition.slideLeftIn');
	$('.carousel-caption p').velocity('transition.slideLeftIn',{ delay: 300 });
	$('.carousel-caption > a').velocity('transition.slideUpIn',{ delay: 600 });
	
	$('#carousel1').on('slide.bs.carousel', function (e) { 
  	  // Select the elements to be animated inside the active slide 
	  $(".carousel-caption h3,.carousel-caption p,.carousel-caption > a").velocity({ opacity: 0 });
  	  $(e.relatedTarget).find('.carousel-caption h3').velocity('transition.slideLeftBigIn',{ delay: 200 });
  	  $(e.relatedTarget).find('.carousel-caption p').velocity('transition.slideLeftBigIn',{ delay: 500 });
    	  $(e.relatedTarget).find('.carousel-caption > a').velocity('transition.slideUpBigIn',{ delay: 700 });
 	 
  	});// End spicing up carousel
  	
  $('form #submit').hover(
 	 function() {$('form #submit').velocity({paddingLeft:10,paddingRight:10});},
  	function(){$('form #submit').velocity('reverse');}
  );
  
   $('#carousel1').hover(
 	 function() {
		 	$('.carousel-indicators').velocity('transition.slideUpIn');
			$('.carousel-control.right').velocity('transition.slideLeftIn');
			$('.carousel-control.left').velocity('transition.slideRightIn');
		 },
  	function(){$('.carousel-indicators,.carousel-control').velocity('reverse');}
  );
  
  $('body').append('<span class="hidden"> <a href="http://ayathemes.com">free animated single page websites</a></span>');
  
  $('#portfolio').mixItUp({
	  animation: {
		easing: 'cubic-bezier(0.175, 0.885, 0.32, 1.275)'
	},
	  selectors: {
		target: '.mix',
		filter: '.filter',
	}
	  });
	  
	 
  	
});