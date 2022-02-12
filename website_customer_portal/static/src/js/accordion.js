(function($) {
    $(document).ready(function() {
        $(".ac-label").click(function(e) {
            e.preventDefault();
            $parent = $(this).parent().parent().parent();
            $article = $parent.find(".ac-content")
            $img = $(this).find("img.noun-arrow-1776263");
            $span = $(this).find("span.ver-pedido");
            if ($article.css('display') == 'block'){
                $article.css("display", 'none');
                $img.css({
                  'transform': 'rotate(0deg)',
                  '-ms-transform': 'rotate(0deg)',
                  '-moz-transform': 'rotate(0deg)',
                  '-webkit-transform': 'rotate(0deg)',
                  '-o-transform': 'rotate(0deg)'
                });
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
                $span.html("Cerrar pedido");
            }
        });
    });
})(jQuery);