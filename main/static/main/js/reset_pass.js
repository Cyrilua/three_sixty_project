$(function () {
    let time;
    let $input = $('.reset-pass-email'),
        $buffer = $('.input-buffer');

    $input.on('input', function () {
        $buffer.text($input.val());
        $input.width($buffer.width());
    });
    setTimeout(timeOut, 1000, $('span.reset-pass-timer'));

    function timeOut(timer) {
        if (typeof(time) == 'undefined') {
            time = timer.text();
        }
        if (timer.text() > 0) {
            timer.text(timer.text() - 1);
            setTimeout(timeOut, 1000, timer);
        } else {
            let el = $('p.reset-pass-repeat-letter')[0];
            const parent = el.parentElement;
            el.remove();
            el = document.createElement('a');
            el.href = '#';
            el.classList.add('reset-pass-repeat-link');
            el.text = 'Отправить письмо ещё раз';
            parent.appendChild(el);
            $('a.reset-pass-repeat-link').click(function () {
                let el = $(this)[0];
                const parent = el.parentElement;
                el.remove();
                el = document.createElement('p')
                el.classList.add('reset-pass-repeat-letter');
                el.innerHTML = 'Отправить письмо ещё раз (доступно через <span class="reset-pass-timer">' + time + '</span> с.)';
                parent.appendChild(el);
                setTimeout(timeOut, 1000, $('span.reset-pass-timer'));
            });
        }
    }
});

