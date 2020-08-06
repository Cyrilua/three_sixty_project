const maxAnswers = 5;
const maxQuestions = 5;
const timeAnimation = 200;

$(function () {
    const body = $('body');
    const pollHeader = $('.poll-editor__header');

    // let questions = {};

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
                document.documentElement.style.setProperty('--mdc-theme-secondary', '#FF1841');
                document.documentElement.style.setProperty('--mdc-theme-text-primary-on-dark', 'white');
            } else if (color === 'blue') {
                document.documentElement.style.setProperty('--mdc-theme-primary', '#001AFF');
                document.documentElement.style.setProperty('--mdc-theme-secondary', '#001AFF');
                document.documentElement.style.setProperty('--mdc-theme-text-primary-on-dark', 'white');
            } else if (color === 'purple') {
                document.documentElement.style.setProperty('--mdc-theme-primary', '#DB00FF');
                document.documentElement.style.setProperty('--mdc-theme-secondary', '#DB00FF');
                document.documentElement.style.setProperty('--mdc-theme-text-primary-on-dark', 'white');
            } else {
                throw new Error('Unexpected attribute on color change');
            }
        } else {
            document.documentElement.style.setProperty('--mdc-theme-primary', '#C4C4C4');
            document.documentElement.style.setProperty('--mdc-theme-secondary', '#C4C4C4');
            document.documentElement.style.setProperty('--mdc-theme-text-primary-on-dark', 'black');
        }
    });

    // Увеличение полей для ввода
    body.on('input', '.textarea-line', function () {
        countLines(this, 5);
    });
    body.on('input', '.textarea-border', function () {
        countLines(this, -1);
    });

    // Настроки ответов типа range
    body.on('change', '.slider-range__min', function () {
        let val = parseInt($(this).val());
        let slider = $(this).closest('.slider-range').children('.mdc-slider');
        let _slider = new mdc.slider.MDCSlider(slider[0]);
        _slider.min = val;
    });
    body.on('change', '.slider-range__max', function () {
        let val = parseInt($(this).val());
        let slider = $(this).closest('.slider-range').children('.mdc-slider');
        let _slider = new mdc.slider.MDCSlider(slider[0]);
        _slider.max = val;
    });
    body.on('change', '.slider-range__step', function () {
        let val = parseInt($(this).val());
        let slider = $(this).closest('.slider-range').children('.mdc-slider');
        let _slider = new mdc.slider.MDCSlider(slider[0]);
        _slider.step = val;
    });

    // Автоувеличение полей ввода
    function countLines(el, delta) {
        el.style.height = '1px';
        el.style.height = (el.scrollHeight + delta) + 'px';
    }

    // Первый запуск
    function run() {
        $('.question').each(function (key, el) {
            // Инициализация типа вопроса
            let sortable = new mdc.select.MDCSelect(el.querySelector('.mdc-select'));
            sortable.listen('MDCSelect:change', () => {
                console.log(sortable.value)
            });
            // Инициализация слайдеров
            if ($(el).attr('data-question-type') === 'range') {
                console.log(el.querySelector('.mdc-slider'))
                let slider = new mdc.slider.MDCSlider(el.querySelector('.mdc-slider'));
                slider.min = parseInt($(el).find('.slider-range__min').val());
                slider.max = parseInt($(el).find('.slider-range__max').val());
                slider.step = parseInt($(el).find('.slider-range__step').val());
                console.log($(el).find('.slider-range__min').val(), $(el).find('.slider-range__max').val(), $(el).find('.slider-range__step').val())
                slider.listen('MDCSlider:change', () => {
                    console.log(`Value changed to ${slider.value}`);
                });
            }
        });
    }
});