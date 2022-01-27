(function($) {
    $(document).ready(function() {
        $(".ac-label").click(function(e) {
            e.preventDefault();
            $check = $(this).parent().parent().prev();
            $img = $(this).find("img");
            $span = $(this).find("span");
            if ($check.prop('checked')){
                $check.prop("checked", false);
                $img.attr("src", "/website_customer_portal/static/src/img/desktop---proyecto-noun-arrow-1776263-1.png");
                $span.html("Ver Pedido");
            } else {
                $check.prop("checked", true);
                $img.attr("src", "/website_customer_portal/static/src/img/desktop---proyecto-noun-arrow-1776263.png");
                $span.html("Cerrar Pedido");
            }
        });
    });
})(jQuery);