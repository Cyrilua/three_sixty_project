const maxAnswers = 5;
const maxQuestions = 5;
const timeAnimation = 200;

$(function () {
    const body = $('body');
    const pollHeader = $('.poll-editor__header');

    // $('.category-content').removeClass('hide');

    // Сортировка
    if ($('.mdc-select').length > 0) {
        const sortable = new mdc.select.MDCSelect(document.querySelector('.mdc-select'));
        sortable.listen('MDCSelect:change', () => {
                console.log(sortable.value)
        });
    }

    // Смена цвета у опроса
    body.on('click', '.color__variable', function () {
        $('.color__variable').removeClass('color__variable--select');
        $(this).addClass('color__variable--select');
        let color = $(this).attr('data-color');
        pollHeader.removeClass('red blue purple');
        if (color !== '') {
            pollHeader.addClass(color)
        }
    });

    // Увеличение полей для ввода
    body.on('input', '.textarea-line', function () {
        countLines(this, 5);
    });

    // Автоувеличение полей ввода
    function countLines(el, delta) {
        el.style.height = '1px';
        el.style.height = (el.scrollHeight + delta) + 'px';
    }
});