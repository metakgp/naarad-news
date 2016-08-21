$(document).ready(function(event){
$("img").addClass('lazy');
 $(".back-to-top").click(function(){
    $(".back-to-top").addClass("animated");
    $(".back-to-top").addClass("rubberBand");
 });
wow = new WOW(
{
animateClass: 'animated',
offset: 100
}
);
wow.init();
$(".navbar-nav li a").click(function(event) {
$(".navbar-collapse").collapse('hide');
});
})

$(document).on('click.card', '.card', function (e) {
if ($(this).find('> .card-reveal').length) {
if ($(e.target).is($('.card-reveal .card-title')) || $(e.target).is($('.card-reveal .card-title i'))) {
$(this).find('.card-reveal').velocity(
{translateY: 0}, {
duration: 225,
queue: false,
easing: 'easeInOutQuad',
complete: function() { $(this).css({ display: 'none'}); }
}
);
}
else if ($(e.target).is($('.card .activator')) ||
$(e.target).is($('.card .activator i')) ) {
$(e.target).closest('.card').css('overflow', 'hidden');
$(this).find('.card-reveal').css({ display: 'block'}).velocity("stop", false).velocity({translateY: '-100%'}, {duration: 300, queue: false, easing: 'easeInOutQuad'});
}
}

$('.card-reveal').closest('.card').css('overflow', 'hidden');
});

$(".scroll").click(function (event) {
event.preventDefault();
var dest = 0;
if ($(this.hash).offset().top > $(document).height() - $(window).height()) {
dest = $(document).height() - $(window).height() + 100;
} else {
dest = $(this.hash).offset().top + 10;
}
$('html,body').animate({
scrollTop: dest
}, 600, 'swing');
dest = dest - 70;
$('html,body').animate({
scrollTop: dest
}, 300, 'swing');
});
 
jQuery(window).load(function() {
jQuery("#status").fadeOut();
jQuery("#preloader").delay(1000).fadeOut("slow");
jQuery("#main-carousel").delay(3000).fadeIn("slow");
})

$(document).ready(function(){
var offset1 = 250;
var offset2 = 250;
var duration = 300;
$(window).scroll(function() {
if (jQuery(this).scrollTop() > offset1) {
$(".back-to-top").fadeIn(duration);
} else {
$(".back-to-top").fadeOut(duration);
}
if (jQuery(this).scrollTop() > offset2) {
$(".on-top-btn").fadeIn(duration);
} else {
$(".on-top-btn").fadeOut(duration);
}
});

$(".back-to-top").click(function(event) {
event.preventDefault();
jQuery('html, body').animate({scrollTop: 0}, duration);
return false;
})
});

var fuse;
var nextQuery = null;
var processing = false;
var currentQuery = null;

$(function() {

 $('#query').focus();

 var worker = new Worker('js/worker2.js');

 $.getJSON("feed.json")
  .success(function(json) {
      worker.postMessage({type: 'data', data: json});
  })
  .error(function(jqxhr, status, err) {
      console.log(jqxhr, status, err);
  });

 worker.onmessage = function(results) {
     processing = false;
     $('#all-div').addClass('hidden');
     displayResults(results.data);
     if (nextQuery !== null) {
         var query = nextQuery;
         nextQuery = null;
         search(query);
     }
 }

 function displayResults(results) {
    var html = ''
    var start = '<section>'
    var end = '</section>'
    var part1 = '<div class="row"><div class="col-md-12 col-sm-12 wow bounceInUp" style="visibility: visible; animation-name: bounceInUp;"><div class="elegant-card border-black z-depth-1"><div class="row"><div class="col-md-12 col-sm-12"><div class="card-footer"><ul class="list-inline"> <li><i class="fa fa-clock-o"></i>Posted on '+results[i].real_date+' at '+results[i].real_time+'</li></ul></div></div>';
    var part2 = ''
    var part3 = ''
    for (var i = 0; i < 20; ++i) {
        if (results[i].pic != "") {
            part2 = '<div class="col-md-4"><div class="card-up view overlay hm-white-slight"><img class="responsive-img lazy" src="'+results[i].pic+'"></div></div><div class="col-md-8"><div class="card-content"><h5>'+results[i].source+'</h5><p>'+results[i].message+'</p></div></div>';
        }
        else {

            part2 ='<div class="col-md-12"><div class="card-content"><h5>'+results[i].source+'</h5><p>'+results[i].message+'</p></div></div>';
        }
        part3 = '<div class="col-md-12 col-sm-12"><div class="card-footer"><ul class="list-inline"><li><a href="https://www.facebook.com/{{ post['id'] }}" target="_blank"><i class="fa fa-facebook"></i> View the post</a></li></ul></div></div></div>';            
        html += (part1 + part2 + part3);
    }
    html = start + html + end;
    $('#result-div').html(html);
    $('#all-div').addClass('hidden');

 }

 var search = _.debounce(function() {
     $('.all-div').addClass('hidden');
     var query = $('#query').val().trim();
     if (query === '') {
         $('.result-div').html('');
         $('.all-div').removeClass('hidden');
         return;
     }
     if (processing) {
         nextQuery = query;
         return;
     }
     if (query === currentQuery) {
         return;
     }
     processing = true;
     currentQuery = query;
     worker.postMessage({type: 'query', query: query});
 }, 200);

 $('#query').keydown(search);

});