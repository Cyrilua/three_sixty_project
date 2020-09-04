$(function () {
    const body = $('body');
    const csrf = $('input[name="csrfmiddlewaretoken"]').val();
    let progress = {};

    run();

    // Сообщение перед ухода со страницы
    window.onunload = function () {
        return confirm('Все несохраненные изменения удалятся')
    };
    window.onbeforeunload = function () {
        return confirm('Все несохраненные изменения удалятся');
    };


    // Увеличение полей для ввода
    body.on('input', '.textarea-line', function () {
        countLines(this, 5);
    });

    // Проверка прогресса
    body.on('click', 'input[type=radio]', function () {
        let name = $(this).attr('name');
        if (!progress[name]) {
            progress[name] = true;
        }
        if (checkProgress(progress)) {
            $('.done-poll').prop({
                'disabled': false,
            })
        }
    });

    body.on('click', '.done-poll', function () {
        ajaxSendResults();
    });

    function ajaxSendResults() {
        let answers = getAnswers();
        console.log(answers)
        let content = $('.taking-poll');
        $.ajax({
            url: 'send/',
            type: 'post',
            data: {
                answers: answers,
                csrfmiddlewaretoken: csrf,
                pollId: content.attr('data-poll-id'),
            },
            beforeSend: function () {
                content.addClass('disabled');
            },
            complete: function () {
                content.removeClass('disabled');
            },
            error: function () {
                Snackbar.show({
                    text: 'Ошибка при отправке результатов',
                    showAction: true,
                    duration: 4000,
                    actionText: "Повторить",
                    actionTextColor: '#5699FF',
                    customClass: 'custom center',
                    onActionClick: function (el) {
                        $(el).animate({
                            opacity: 0,
                        }, 200, function () {
                            ajaxSendResults();
                        })
                    },
                });
            },
            success: function () {
                window.onunload = window.onbeforeunload = function () {
                };
                location.href = '/polls/';
            },
        });
    }

    function checkProgress(progress) {
        let keys = Object.keys(progress);
        for (let k in keys) {
            if (!progress[keys[k]]) return false;
        }
        return true;
    }

    // Автоувеличение полей ввода
    function countLines(el, delta) {
        el.style.height = '1px';
        el.style.height = (el.scrollHeight + delta) + 'px';
    }

    function run() {
        // Изменение цвета
        let currentColor = $('.taking-poll').attr('data-color');
        let questions = $('.question')
        if (currentColor === 'blue') {
            document.documentElement.style.setProperty('--mdc-theme-primary', '#001AFF');
            document.documentElement.style.setProperty('--mdc-theme-secondary', '#001AFF');
            document.documentElement.style.setProperty('--mdc-theme-text-primary-on-dark', 'white');
        } else if (currentColor === 'red') {
            document.documentElement.style.setProperty('--mdc-theme-primary', '#FF1841');
            document.documentElement.style.setProperty('--mdc-theme-secondary', '#FF1841');
            document.documentElement.style.setProperty('--mdc-theme-text-primary-on-dark', 'white');
        } else if (currentColor === 'purple') {
            document.documentElement.style.setProperty('--mdc-theme-primary', '#DB00FF');
            document.documentElement.style.setProperty('--mdc-theme-secondary', '#DB00FF');
            document.documentElement.style.setProperty('--mdc-theme-text-primary-on-dark', 'white');
        } else {
            document.documentElement.style.setProperty('--mdc-theme-primary', '#C4C4C4');
            document.documentElement.style.setProperty('--mdc-theme-secondary', '#C4C4C4');
            document.documentElement.style.setProperty('--mdc-theme-text-primary-on-dark', 'black');
        }

        questions.each(function (key, el) {
            // Инициализация слайдеров
            let qType = $(el).attr('data-question-type');
            if (qType === 'range') {
                sliderDeclaration(el);
            }

            // Заполнение прогресса (только radio)
            if (qType === 'radio') {
                progress[$(el).children('.question__answers').children('.answer').children('.radio').children('.mdc-radio').children('input[type=radio]').attr('name')] = false;
            }

        });
        if (Object.keys(progress).length === 0) {
            $('.done-poll').prop({
                'disabled': false,
            });
        }
    }

    function sliderDeclaration(el) {
        let slider = new mdc.slider.MDCSlider(el.querySelector('.mdc-slider'));
        slider.listen('MDCSlider:change', () => {
            // console.log(`Value changed to ${slider.value}`);
        });
    }

    function getAnswers() {
        let answers = [];

        let questions = $('.question');
        questions.each(function (key, el) {
            let type = $(el).attr('data-question-type');
            let answer = {
                id: $(el).attr('data-real-id'),
                type: type,
            };
            let value;
            if (type === 'radio') {
                value = $(el).children('.question__answers').children('.answer').children('.radio').children('.mdc-radio').children('input[type=radio]:checked').attr('data-real-id');
            } else if (type === 'checkbox') {
                value = [];
                let checked = $(el).children('.question__answers').children('.answer').children('.checkbox').children('.mdc-checkbox').children('input[type=checkbox]:checked');
                checked.each(function (key, el) {
                    value.push($(el).attr('data-real-id'));
                });
            } else if (type === 'openQuestion') {
                value = $(el).children('.open-answer').children('.answer').val();
            } else if (type === 'range') {
                value = $(el).children('.range-answer').children('.mdc-slider').attr('aria-valuenow');
            } else {
                throw new Error('unexpected attribute when sending results');
            }
            answer.value = value;
            answers.push(answer);
        });

        return answers;
    }
});