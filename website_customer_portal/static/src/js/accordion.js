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
                $img.removeClass("rotate-image");
                $span.html("Ver pedido");
            } else {
                $article.css("display", 'block');
                $img.addClass("rotate-image");
                $span.html("Cerrar pedido");
            }
        });
    });
})(jQuery);