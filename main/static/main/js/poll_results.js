$(function () {
    const body = $('body');
    const csrf = $('input[name="csrfmiddlewaretoken"]').val();

    run();

    // Назад к шаблонам
    body.on('click', '.menu__back', function () {
        location.href = '/polls/';
    });

    // Сохранить как шаблон
    body.on('click', '#saveAs', function () {
        ajaxSaveAs();
    });

    function ajaxSaveAs() {
        let template = getTemplate();
        // let status = $(this).parent().children('.save__status');
        let results = $('.results');
        console.log(template)
        $.ajax({
            url: 'save_as/',
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
                template: template,
            },
            beforeSend: function () {
                results.addClass('disabled');
                // status.removeClass('status--loading status--error status--done')
                //     .addClass('status--loading');
            },
            success: function () {
                // status.removeClass('status--loading status--error status--done')
                //     .addClass('status--done');
                Snackbar.show({
                    text: 'Шаблон успешно создан',
                    showAction: true,
                    duration: 3000,
                    actionText: "Закрыть",
                    actionTextColor: 'green',
                    customClass: 'custom',
                });
            },
            error: function () {
                // status.removeClass('status--loading status--error status--done')
                //     .addClass('status--error');
                Snackbar.show({
                    text: 'Ошибка при сохранении шаблона',
                    showAction: true,
                    duration: 3000,
                    actionText: "Повторить",
                    actionTextColor: 'red',
                    customClass: 'custom',
                    onActionClick: function (el) {
                        $(el).animate({
                            opacity: 0,
                        }, 200, function () {
                            // el.remove()
                            ajaxSaveAs();
                        })
                    },
                });
            },
            complete: function () {
                results.removeClass('disabled');
            }
        })
    }

    function run() {
        let statistics = $('.question__statistics-answers');
        statistics.each(function (key, el) {
            let variables = $(el).children('.statistics-answer');
            let widthVariables = Math.ceil(el.offsetWidth / variables.length / 3 * 2);
            console.log(variables.length)
            variables.each(function (key, elem) {
                let percent = $(elem).children('.percent').text();
                let height = el.offsetHeight / 100 * percent;
                elem.style.width = widthVariables + 'px';
                elem.style.height = height + 'px';
            })
        });
    }

    function getTemplate() {
        let poll = $('.poll');
        let questions = poll.children('.questions').children('.question');

        let template = {
            name: poll.children('.poll__name').text(),
            description: poll.children('.poll_description').text(),
            questions: [],
            color: poll.attr('data-poll-color'),
            countQuestion: questions.length,
        };
        questions.each(function (key, el) {
            let type = $(el).attr('data-question-type');
            template.questions.push({
                id: $(el).attr('data-question-id'),
                serialNumber: key + 1,
                type: type,
                name: $(el).children('.question__head').children('.question__name ').text(),
            });
            if (type === 'radio' || type === 'checkbox') {
                let answersBlock = $(el).children('.question__answers');
                let answers = answersBlock.children('.answer');
                template.questions[key].answers = [];
                template.questions[key].countAnswers = answers.length;
                $(answers).each(function (keyA, elA) {
                    let answerText = $(elA).children('.answer__text').text();
                    template.questions[key].answers.push(answerText);
                })
            } else if (type === 'range') {
                let answersBlock = $(el).children('.question__statistics-answers');
                let answers = answersBlock.children('.statistics-answer');
                let min = answers.first().children('.value').text();
                let max = answers.last().children('.value').text();
                // let step = Math.ceil((max - min) / answers.length);     // МОГУТ БЫТЬ НЕТОЧНОСТИ
                let step = Math.max((answers[1] - answers[0]), (answers[2] - answers[1]));      // Вариант получше
                template.questions[key].settingsSlider = {
                    min: min,
                    max: max,
                    step: step,
                }
            } else if (type === 'openQuestion') {
            } else {
                throw new Error('unexpected attribute when receiving a poll');
            }
        });
        return template;
    }
});