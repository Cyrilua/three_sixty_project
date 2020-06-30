$(function () {
    let $input = $('.reset-pass-email'),
        $buffer = $('.input-buffer');

    // Авторасширение поля для ввода
    $input.on('input', function () {
        $buffer.text($input.val());
        $input.width($buffer.width());
        sessionStorage.setItem('emailForResetPass', $input.val());
    });
});

