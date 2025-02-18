$(function () {
    const timeShow = 300;
    let btn = $('.reset-pass-confirm-next');
    let pass1 = $('#id_new_password1');
    let pass2 = $('#id_new_password2');
    let body = $('body');

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

    pass1.on('input', function () {
        let popup = $(this).parent().children('.popup');
        popup.addClass('old');
        $(this).removeClass('error');
        popup.stop().animate({
            opacity: 0,
        }, timeShow, function () {
            $(this).remove();
        });
        checkBtn(pass1, pass2, btn);
    });

    pass2.on('input', function () {
        checkBtn(pass1, pass2, btn);
    })
});

function checkBtn(pass1, pass2, btn) {
    if (pass1.val().length > 0 && pass2.val().length > 0)
        btn.prop({'disabled': false});
    else
        btn.prop({'disabled': true});
}