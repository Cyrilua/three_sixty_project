const maxAnswers = 5;
const maxQuestions = 5;
const timeAnimation = 200;

$(function () {
    const body = $('body');
    const pollHeader = $('.poll-editor__header');

    // let questions = {};


    // $('.category-content').removeClass('hide');

    run();

    // Смена цвета у опроса
    body.on('click', '.color__variable', function () {
        $('.color__variable').removeClass('color__variable--select');
        $(this).addClass('color__variable--select');
        let color = $(this).attr('data-color');
        pollHeader.removeClass('red blue purple');
        if (color !== '') {
            pollHeader.addClass(color);
            if (color === 'red') {
                document.documentElement.style.setProperty('--mdc-theme-primary', '#FF1841');
            } else if (color === 'blue') {
                document.documentElement.style.setProperty('--mdc-theme-primary', '#001AFF');
            } else if (color === 'purple') {
                document.documentElement.style.setProperty('--mdc-theme-primary', '#DB00FF');
            } else {
                throw new Error('Unexpected attribute on color change');
            }
        } else {
            document.documentElement.style.setProperty('--mdc-theme-primary', '#C4C4C4');
        }
    });

    // Увеличение полей для ввода
    body.on('input', '.textarea-line', function () {
        countLines(this, 5);
    });

    body.on('input', '.textarea-border', function () {
        countLines(this, -1);
    });

    // Автоувеличение полей ввода
    function countLines(el, delta) {
        el.style.height = '1px';
        el.style.height = (el.scrollHeight + delta) + 'px';
    }

    function run() {
        // Инициализация сортировки
        $('.question').each(function (key, el) {
            // let numberQuestion = el.getAttribute('data-question');
            let sortable = new mdc.select.MDCSelect(el.querySelector('.mdc-select'));
            sortable.listen('MDCSelect:change', () => {
                console.log(sortable.value)
            });
            // questions[`question_${numberQuestion}`] = {
            //     'sortable': sortable,
            // };
        });
    }
});