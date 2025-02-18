$(function () {
    const timeShow = 300;
    const body = $('body');

    body.on('focus', '.input-field', function () {
        let popup = $(this).parent().children('.popup');
        if (!popup.hasClass('old')) {
            popup.css({
                display: 'block',
                opacity: 0,
            })
                .stop().animate({
                opacity: 1,
            }, timeShow);
        }
    });

    body.on('focusout', '.input-field', function () {
        let popup = $(this).parent().children('.popup');
        if (!popup.hasClass('old')) {
            popup.stop().animate({
                opacity: 0,
            }, timeShow, function () {
                $(this).css({
                    display: 'none',
                });
            });
        }
    });
    
    body.on('input', '.input-field', function () {
        let popup = $(this).parent().children('.popup');
        popup.addClass('old');
        $(this).removeClass('error');
        popup.stop().animate({
            opacity: 0,
        }, timeShow, function () {
            $(this).remove();
        })
    });

    $('.popup').parent().children('.error').focus();
});