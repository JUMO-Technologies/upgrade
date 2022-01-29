(function($) {
    $(document).ready(function() {
        var orders = $(".desktopproyecto .order-container")
        var height = 0;
        var length = orders.length;
        if(orders.length == 0) {
            orders = $(".desktopinicio .proyecto");
            var length = orders.length - 4;
            if(length < 0){
                length = 0;
            }
        }
        $overlap = $("div.overlap-group6");
        if(!$overlap){
            $overlap = $("div.overlap-group1");
        }
        if(orders.length > 0){
            height = orders[0].clientHeight;
        }
        if($overlap.length > 0){
            $overlap.css("height", ($overlap[0].clientHeight + length * height) + "px");
        }
        $(".ac-label").click(function(e) {
            e.preventDefault();
            $parent = $(this).parent().parent().parent();
            $article = $parent.find(".ac-content")
            $img = $(this).find("img");
            $span = $(this).find("span");
            $overlap = $("div.overlap-group6");
            if ($article.css('display') == 'block'){
                var art_before = $article[0].scrollHeight;
                $article.css("display", 'none');
                $img.css({
                  'transform': 'rotate(0deg)',
                  '-ms-transform': 'rotate(0deg)',
                  '-moz-transform': 'rotate(0deg)',
                  '-webkit-transform': 'rotate(0deg)',
                  '-o-transform': 'rotate(0deg)'
                });
                $overlap.css('height', ($overlap[0].clientHeight - art_before) + "px");
                $span.html("Ver pedido");
            } else {
                $article.css("display", 'block');
                $img.css({
                  'transform': 'rotate(180deg)',
                  '-ms-transform': 'rotate(180deg)',
                  '-moz-transform': 'rotate(180deg)',
                  '-webkit-transform': 'rotate(180deg)',
                  '-o-transform': 'rotate(180deg)'
                });
                $overlap.css('height', ($overlap[0].clientHeight + $article[0].scrollHeight) + "px");
                $span.html("Cerrar Pedido");
            }
        });
    });
})(jQuery);