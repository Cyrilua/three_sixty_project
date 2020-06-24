$(function () {
    let $input = $('.reset-pass-email'),
        $buffer = $('.input-buffer');

    $input.on('input', function () {
        $buffer.text($input.val());
        $input.width($buffer.width());
    });

    setTimeout(timeOut, 1000, $('.reset-pass-timer'));
});

function timeOut(timer) {
    if (timer.text() > 0) {
        timer.text(timer.text() - 1);
        setTimeout(timeOut, 1000, timer);
    } else {
        $('.reset-pass-repeat-letter')
            .text("Отправить письмо ещё раз")
            .prop({
                'href': '#',
            });
    }
}