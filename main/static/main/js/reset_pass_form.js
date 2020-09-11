$(function () {
    let $input = $('.reset-pass-email'),
        $buffer = $('.input-buffer');
    let btn = $('.reset-pass-next');

    // Проверка заполненности поля
    $('.input-field').on('input', function () {
        if ($(this).val().length > 0)
            btn.prop({'disabled': false});
        else
            btn.prop({'disabled': true});
    });

    // Авторасширение поля для ввода
    $input.on('input', function () {
        $buffer.text($input.val());
        $input.width($buffer.width());
        sessionStorage.setItem('emailForResetPass', $input.val());
    });

    // Очистка памяти
    $('#logo, #login, #logout, #register').click(function () {
        if (sessionStorage.getItem('emailForResetPass').length){
            sessionStorage.removeItem('emailForResetPass');
        }
    });
});

