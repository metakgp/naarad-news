wow = new WOW(
{
animateClass: 'animated',
offset: 100
}
);
wow.init();

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
     $('.all-div').addClass('hidden');
     displayResults(results.data);
     if (nextQuery !== null) {
         var query = nextQuery;
         nextQuery = null;
         search(query);
     }
 }

 function displayResults(results) {
     var html = ''
     var part1 = '<div class="row"><div class="col-md-12 col-sm-12 wow bounceInUp" style="visibility: visible; animation-name: bounceInUp;"><div class="elegant-card border-black z-depth-1">';
     var part2 = ''
     var part3 = ''
     for (var i = 0; i < 20; ++i) {
         if (results[i].pic != "") {
            part2 = '<div class="col-md-4"><div class="card-up view overlay hm-white-slight"><img class="responsive-img lazy" src="'+results[i].pic+'"></div></div><div class="col-md-8"><div class="card-content"><h5>'+results[i].source+'</h5><p>'+results[i].message+'</p></div></div>';
        }
        else {

            part2 ='<div class="col-md-12"><div class="card-content"><h5>'+results[i].source+'</h5><p>'+results[i].message+'</p></div></div>';
        }
        part3 = '<div class="col-md-12"><div class="card-footer"><ul class="list-inline"><li class="left col-md-4"><i class="fa fa-clock-o"></i>Posted at '+results[i].created_time+'</li><li class="right col-md-4 col-md-offset-4"><a href="https://www.facebook.com/'+results[i].id+'" target="_blank"><i class="fa fa-facebook"></i> View the post</a></li></ul></div></div></div></div></div>';            
        html += (part1 + part2 + part3);
    }
     $('.result-div').html(html);
     $('.all-div').addClass('hidden');

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