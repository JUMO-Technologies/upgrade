(function($) {
    $(document).ready(function() {
        $(".ac-label").click(function(e) {
            e.preventDefault();
            $check = $(this).parent().parent().prev();
            $icon = $(this).find("i");
            $span = $(this).find("span");
            if ($check.prop('checked')){
                $check.prop("checked", false);
                $icon.removeClass("fa-angle-up");
                $icon.addClass("fa-angle-down");
                $span.html("Ver Pedido");
            } else {
                $check.prop("checked", true);
                $icon.removeClass("fa-angle-down");
                $icon.addClass("fa-angle-up");
                $span.html("Cerrar Pedido");
            }
        });

    });
})(jQuery);