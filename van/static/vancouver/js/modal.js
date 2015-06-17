$(".modal-wide").on("show.bs.modal", function() {
	var height = $(window).height() - 200;
	$(this).find(".modal-body").css("max-height", height);
});

// var tableOffset = $("#table-1").offset().top;
// var $header = $("#table-1 > thead").clone();
// var $fixedHeader = $("#header-fixed").append($header);

// $(window).bind("scroll", function() {
//     var offset = $(this).scrollTop();

//     if (offset >= tableOffset && $fixedHeader.is(":hidden")) {
//         $fixedHeader.show();
//     }
//     else if (offset < tableOffset) {
//         $fixedHeader.hide();
//     }
// });