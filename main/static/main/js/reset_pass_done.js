$(function () {
    let time;

    // Обратный таймер - рестрат письма на email
    setTimeout(timeOut, 1000, $('span.reset-pass-timer'));

    function timeOut(timer) {
        if (typeof (time) == 'undefined') {
            time = timer.text();
        }
        if (timer.text() > 0) {
            timer.text(timer.text() - 1);
            setTimeout(timeOut, 1000, timer);
        } else {
            let el = $('p.reset-pass-repeat-letter')[0];
            const parent = el.parentElement;
            el.remove();
            let input = $("#id_email");
            input.val(sessionStorage.getItem('emailForResetPass'));
            el = document.createElement('a');
            el.href = '#';
            el.classList.add('reset-pass-repeat-link');
            el.text = 'Отправить письмо ещё раз';
            parent.append(el);
            $('a.reset-pass-repeat-link').click(function () {
                let el = $(this)[0];
                let form = el.parentElement.parentElement;
                form.submit();
            });
        }
    }
});

