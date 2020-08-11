$(function () {
    const maxAnswers = 15;
    const maxQuestions = 50;
    const maxLengthInput = 150;
    const timeAnimation = 200;

    const body = $('body');
    const editor = $('.editor ');
    const menu = $('.menu-r').children('.menu').children('.menu__item');
    const csrf = $('input[name="csrfmiddlewaretoken"]').val();
    let listKeys = [];
    let accessStep3 = false;
    let pollId;

    run();

    // Смена цвета у опроса
    body.on('click', '.color__variable', function () {
        $('.color__variable').removeClass('color__variable--select');
        $(this).addClass('color__variable--select');
        let color = $(this).attr('data-color');
        let pollHeader = $('.poll-editor__header');
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
    body.on('change, input', '.slider-range__min', function () {
        let settings = $(this).parent().parent();
        let min = parseInt($(this).val());
        let max = parseInt(settings.children('.max').children('.slider-range__max').val());
        let step = parseInt(settings.children('.step').children('.slider-range__step').val());
        if (min < 0) {
            min = 0;
        } else if (min > max - step) {
            min = max - step;
        } else if (typeof (min) !== typeof (10) || isNaN(min)) {
            min = 0;
        }
        $(this).val(min);
        if (min >= 0 && min <= 100) {
            let slider = $(this).closest('.slider-range').children('.mdc-slider');
            let _slider = new mdc.slider.MDCSlider(slider[0]);
            _slider.step = step;
            _slider.max = max;
            _slider.min = min;
            // console.log(min, max, step, "maxStep")

            // console.log(_slider.min, _slider.max, _slider.step, "maxStep")
        }
    });
    body.on('change, input', '.slider-range__max', function () {
        let settings = $(this).parent().parent();
        let max = parseInt($(this).val());
        let min = parseInt(settings.children('.min').children('.slider-range__min').val());
        let step = parseInt(settings.children('.step').children('.slider-range__step').val());
        if (max < min + step) {
            // console.log(1)
            max = min + step;
        } else if (max > 100) {
            // console.log(2)
            max = 100;
        } else if (typeof (max) !== typeof (10) || isNaN(max)) {
            // console.log(3)
            max = 100;
        }
        $(this).val(max);
        if (max >= 1 && max <= 100) {
            let slider = $(this).closest('.slider-range').children('.mdc-slider');
            let _slider = new mdc.slider.MDCSlider(slider[0]);
            _slider.step = step;
            _slider.max = max;
            _slider.min = min;
            // console.log(min, max, step, "maxStep")

            // console.log(_slider.min, _slider.max, _slider.step, "maxStep")
        }
    });
    body.on('change, input', '.slider-range__step', function () {
        let settings = $(this).parent().parent();
        let step = parseInt($(this).val());
        let max = parseInt(settings.children('.max').children('.slider-range__max').val());
        let min = parseInt(settings.children('.min').children('.slider-range__min').val());
        let maxStep = max - min;
        if (step < 1) {
            step = 1;
        } else if (step > 50) {
            step = 50;
        } else if (step > maxStep) {
            step = maxStep;
        } else if (typeof (step) !== typeof (10) || isNaN(step)) {
            step = 1;
        }
        $(this).val(step);
        if (step >= 1 && step <= 50) {
            let slider = $(this).closest('.slider-range').children('.mdc-slider');
            let _slider = new mdc.slider.MDCSlider(slider[0]);
            _slider.step = step;
            _slider.max = max;
            _slider.min = min;
            // console.log(min, max, step, maxStep)

            // console.log(_slider.min, _slider.max, _slider.step, maxStep)
        }
    });

    // Удаление вопросов
    body.on('click', '.question__urn', function () {
        let question = $(this).parent().parent();
        let questions = $(question).parent();
        if (questions.children('.question').length === maxQuestions) {
            // console.log(questions.parent().children('.actions').children('.plus'))
            questions.parent().children('.actions').children('.plus').removeClass('hide')
        }
        let id = question.attr('data-question-id');
        // // Удаляем из listQuestions
        let i = listKeys.indexOf(id);
        if (i !== -1) delete listKeys[i];
        // delete listQuestions[id];
        question.remove();
        if (questions.children('.question').length === 0) {
            $('#nextToStep2').prop({
                'disabled': true,
            });
            menu.eq(1).addClass('disabled');
            if (accessStep3) {
                menu.eq(2).addClass('disabled');
            }
            $('.save-as').css("visibility", "hidden");
            // let newQuestion = createNewQuestion();
            // console.log(newQuestion)
            // questions.append(newQuestion);
        }
        // console.log(listQuestions)
    });

    // Добавеление вопросов
    body.on('click', '.plus', function () {
        let questions = $('.questions');
        let newQuestion = createNewQuestion();
        // console.log(newQuestion)
        questions.append(newQuestion);
        $('#nextToStep2').prop({
            'disabled': false,
        });
        menu.eq(1).removeClass('disabled');
        if (accessStep3) {
            menu.eq(2).removeClass('disabled');
        }
        $('.save-as').css("visibility", "visible");
        // Заносим в listKeys
        listKeys.push($(newQuestion).attr('data-question-id'));
        // console.log(listQuestions)

        if (questions.children('.question').length >= maxQuestions) {
            $(this).addClass('hide');
        }
    });

    // Добавление варианта ответа
    body.on('click', '.new-answer__btn', function () {
        let question = $(this).parent();
        let qType = question.attr('data-question-type');
        if (qType === 'radio' || qType === 'checkbox') {
            let answers = question.children('.question__answers');
            answers.append(createNewAnswer(qType));
            if (answers.children('.answer').length >= maxAnswers) {
                $(this).addClass('hide');
            }
        } else {
            throw new Error('Unexpected attribute when adding answer option');
        }
    });

    // Удалене варианта ответа
    body.on('click', '.answer__clear', function () {
        let answer = $(this).parent();
        let answers = answer.parent();
        let question = answers.parent();
        let qType = question.attr('data-question-type');
        if (qType === 'radio' || qType === 'checkbox') {
            let length = answers.children('.answer').length;
            if (length === maxAnswers) {
                question.children('.new-answer__btn').removeClass('hide');
            } else if (length === 1) {
                // answers.append(createNewAnswer(qType));
                answer.children('.answer__text').val('');
                return;
            }
            answer.remove();
        } else {
            throw new Error('Unexpected attribute when adding answer option');
        }
    });

    // Отмена созданияF
    body.on('click', '#cancel', function () {
        location.href = '/polls/';
    });

    // Сохранения шаблона
    body.on('click', '#saveAs', function () {
        let template = getTemplate();
        let status = $(this).parent().children('.save__status');
        console.log(template)
        $.ajax({
            url: 'save_as/',
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
                pollId: pollId,
                template: template,
            },
            beforeSend: function () {
                menu.addClass('disabled');
                editor.addClass('disabled');
                status.removeClass('status--loading status--error status--done')
                    .addClass('status--loading');
            },
            success: function () {
                status.removeClass('status--loading status--error status--done')
                    .addClass('status--done');
            },
            error: function () {
                status.removeClass('status--loading status--error status--done')
                    .addClass('status--error');
            },
            complete: function () {
                menu.eq(0).removeClass('disabled');
                menu.eq(1).removeClass('disabled');
                if (accessStep3) {
                    menu.eq(2).removeClass('disabled');
                }
                editor.removeClass('disabled');
            }
        })
    });

    // body.on('focusout', '.question', function () {
    //     console.log('focusout')
    // })

    // С 1 шага на 2
    body.on('click', '#nextToStep2', function (el) {
        ajaxStepFrom1To2(el);
    });

    function ajaxStepFrom1To2(el) {
        let id = editor.attr('data-poll-id');
        let template = getTemplate();
        console.log(template)
        $.ajax({
            url: 'step/2/from/1/',
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
                pollId: pollId,
                template: template,
            },
            beforeSend: function () {
                // $(el.target).prop({
                //     'disabled': true,
                // });
                editor.addClass('disabled');
                menu.addClass('disabled');
            },
            success: function (response) {
                document.documentElement.style.setProperty('--mdc-theme-primary', '#FF1841');
                document.documentElement.style.setProperty('--mdc-theme-secondary', '#FF1841');
                document.documentElement.style.setProperty('--mdc-theme-text-primary-on-dark', 'white');

                let headMain = $('.head__main');
                headMain.empty();
                headMain[0].insertAdjacentHTML('afterbegin', response.headMain);

                let headMove = $('.head__move');
                headMove.empty();
                headMove[0].insertAdjacentHTML('afterbegin', response.headMove);

                let categories = $('.categories-block');
                categories.empty();
                categories[0].insertAdjacentHTML('afterbegin', response.categories);

                if (pollId === undefined) {
                    pollId = response.pollId;
                }

                editor.attr({
                    'data-step': '2',
                });

                menu.eq(0).removeClass('item--active');
                menu.eq(1).addClass('item--active');
            },
            complete: function () {
                // $(el.target).prop({
                //     'disabled': false,
                // });
                editor.removeClass('disabled');
                menu.eq(1).removeClass('disabled');
                menu.eq(0).removeClass('disabled');
                if (accessStep3) {
                    menu.eq(2).removeClass('disabled');
                }
            },
            error: function () {
            },
        });
    }

    // С 2 шага на 1
    body.on('click', '#backToStep1', function (el) {
        ajaxStepFrom2To1(el);
    });

    function ajaxStepFrom2To1(el) {
        let checkedTarget = $('input[name=participants]:checked').attr('data-participant-id');
        $.ajax({
            url: 'step/1/from/2/',
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
                checkedTarget: checkedTarget,
                pollId: pollId,
            },
            beforeSend: function () {
                // $(el.target).prop({
                //     'disabled': true,
                // });
                menu.addClass('disabled');
                editor.addClass('disabled');
            },
            success: function (response) {
                let headMain = $('.head__main');
                headMain.empty();
                headMain[0].insertAdjacentHTML('afterbegin', response.headMain);

                let headMove = $('.head__move');
                headMove.empty();
                headMove[0].insertAdjacentHTML('afterbegin', response.headMove);

                let categories = $('.categories-block');
                categories.empty();
                categories[0].insertAdjacentHTML('afterbegin', response.categories);

                editor.attr({
                    'data-step': '1',
                });

                menu.eq(1).removeClass('item--active');
                menu.eq(0).addClass('item--active');

                run();
            },
            complete: function () {
                // $(el.target).prop({
                //     'disabled': false,
                // });
                menu.eq(0).removeClass('disabled');
                menu.eq(1).removeClass('disabled');
                if (accessStep3) {
                    menu.eq(2).removeClass('disabled');
                }
                editor.removeClass('disabled');
            },
        });
    }

    // 2 и 3 шаг, смена категорий (участники/команды)
    let timeOutId;
    body.on('click', '.category', function () {
        let partUrl = $(this).attr('data-part-url');
        let updater = $('.loader-round');
        let loader = $('.loader__status');
        let substrate = $('.substrate');
        let search = $('.input__search');
        let step = editor.attr('data-step');
        if (step !== 2 || step !== 3) {
            throw new Error('Unexpected attribute on search');
        }
        let data;
        if (step === 2) {
            let checkedTarget = $('input[name=participants]:checked').attr('data-participant-id');
            data = {
                pollId: pollId,
                csrfmiddlewaretoken: csrf,
                checkedTarget: checkedTarget,
            }
        } else if (step === 3) {
            let checkedInterviewed = [];
            $('input[name=participants]:checked').each(function (key, elem) {
                checked.push($(elem).attr('data-participant-id'));
            });
            data = {
                pollId: pollId,
                csrfmiddlewaretoken: csrf,
                checkedInterviewed: checkedInterviewed,
            }
        }
        $.ajax({
            url: `step/${step}/category/${partUrl}/`, // step = 2 | 3,  partUrl = participants | teams
            type: 'post',
            data: data,
            beforeSend: function () {
                clearTimeout(timeOutId);
                substrate.addClass('disabled');
                updater.removeClass('hide');
                loader
                    .removeClass('status--loading status--done status--error')
                    .addClass('status--loading');
                menu.addClass('disabled');
                editor.addClass('disabled');
            },
            success: function (response) {
                if (partUrl === 'participants') {
                    search.attr({
                        'placeholder': 'Поиск по участникам...',
                        'data-mode': 'participants',
                    });
                } else if (partUrl === 'teams') {
                    search.attr({
                        'placeholder': 'Поиск по командам...',
                        'data-mode': 'teams',
                    });
                } else {
                    throw new Error('unexpected attribute when changing category');
                }
                search.prop({
                    'disabled': false,
                });

                let content = $('.content');
                content.empty();
                content[0].insertAdjacentHTML('afterbegin', response.content);
                loader
                    .removeClass('status--loading status--done status--error')
                    .addClass('status--done');

                if ($('input[name=participants]:checked').length > 0) {
                    if (step === 2) {
                        $('#nextToStep3').prop({
                            'disabled': false,
                        });
                    } else if (step === 3) {
                        $('#sendPoll').prop({
                            'disabled': false,
                        });
                    }
                } else {
                    if (step === 2) {
                        $('#nextToStep3').prop({
                            'disabled': true,
                        });
                    } else if (step === 3) {
                        $('#sendPoll').prop({
                            'disabled': true,
                        });
                    }
                }
            },
            complete: function () {
                substrate.removeClass('disabled');
                timeOutId = setTimeout(function () {
                    loader.removeClass('status--loading status--done status--error');
                    updater.addClass('hide');
                }, 2000);
                menu.eq(0).removeClass('disabled');
                menu.eq(1).removeClass('disabled');
                if (accessStep3) {
                    menu.eq(2).removeClass('disabled');
                }
                editor.removeClass('disabled');
            },
            error: function () {
                search.prop({
                    'disabled': true,
                });
                loader
                    .removeClass('status--loading status--done status--error')
                    .addClass('status--error');
            }
        })
    });

    // 2 шаг - При выборе цели можно нажать кнопку ДАЛЕЕ
    body.on('click', '[name=participants]', function () {
        $('#nextToStep3').prop({
            'disabled': false,
        });
        accessStep3 = true;
        menu.eq(2).addClass('disabled');
    });

    // С 2 шага на 3
    body.on('click', '#nextToStep3', function (el) {
        ajaxStepFrom2To3(el);
    });

    function ajaxStepFrom2To3(el) {
        let checkedTarget = $('input[name=participants]:checked').attr('data-participant-id');
        $.ajax({
            url: 'step/3/from/2/',
            type: 'post',
            data: {
                pollId: pollId,
                csrfmiddlewaretoken: csrf,
                checkedTarget: checkedTarget,
            },
            beforeSend: function () {
                // $(el.target).prop({
                //     'disabled': true,
                // });
                menu.addClass('disabled');
                editor.addClass('disabled');
            },
            success: function (response) {
                let headMain = $('.head__main');
                headMain.empty();
                headMain[0].insertAdjacentHTML('afterbegin', response.headMain);

                let headMove = $('.head__move');
                headMove.empty();
                headMove[0].insertAdjacentHTML('afterbegin', response.headMove);

                let categories = $('.categories-block');
                categories.empty();
                categories[0].insertAdjacentHTML('afterbegin', response.categories);

                editor.attr({
                    'data-step': '3',
                });

                menu.eq(1).removeClass('item--active');
                menu.eq(2).addClass('item--active');
            },
            complete: function () {
                // $(el.target).prop({
                //     'disabled': false,
                // });
                menu.removeClass('disabled');
                editor.removeClass('disabled');
            },
            error: function () {
            },
        });
    }

    // 2 и 3 шаг - выбор по командам - свернуть/развернуть команду
    body.on('click', '.team__action', function () {
        let team = $(this).parent().parent().parent();
        let teamId = team.attr('data-team-id');
        $('.team--selected').each(function (key, el) {
            let elId = $(el).attr('data-team-id');
            if (teamId !== elId) {
                $(el).toggleClass('team--selected');
            }
        });
        team.toggleClass('team--selected');
    });

    // Шаг 2 и 3 - Поиск по командам/участникам
    let ajaxSearch;
    body.on('input', '.input__search', function (el) {
        let sort = $('.sort');
        let content = $('.content');
        let loader = $('.loader-round');
        let loaderStatus = loader.children('.loader__status');
        let step = editor.attr('data-step');
        if (step !== 2 || step !== 3) {
            throw new Error('Unexpected attribute on search');
        }
        let data;
        if (step === 2) {
            data = {
                pollId: pollId,
                csrfmiddlewaretoken: csrf,
                mode: $(el.target).attr('data-mode'),   // mode = participant | teams
                checkedTarget: $('input[name=participants]:checked').attr('data-participant-id'),
            }
        } else if (step === 3) {
            let checkedInterviewed = [];
            $('input[name=participants]:checked').each(function (key, elem) {
                checked.push($(elem).attr('data-participant-id'));
            });
            data = {
                pollId: pollId,
                csrfmiddlewaretoken: csrf,
                mode: $(el.target).attr('data-mode'),   // mode = participant | teams
                checkedInterviewed: checkedInterviewed,
            }
        }
        ajaxSearch = $.ajax({
            url: `step/${step}/search/`,
            type: 'post',
            data: data,
            beforeSend: function () {
                if (ajaxSearch) {
                    ajaxSearch.abort()
                }
                loader.removeClass('hide');
                loaderStatus
                    .removeClass('status--loading status--done status--error')
                    .addClass('status--loading');
                sort.addClass('disabled');
                content.empty();
            },
            complete: function () {
                ajaxSearch = undefined;
                sort.removeClass('disabled');
                loader.addClass('hide');
                loaderStatus
                    .removeClass('status--loading status--done status--error')
            },
            success: function (response) {
                content[0].insertAdjacentHTML('afterbegin', response.content);
            }
        })
    });

    // 3 шаг - активация кнопки ОТПРАВИТЬ
    body.on('click', '[name=participants]', function () {
        if ($('input[name=participants]:checked').length > 0) {
            $('#sendPoll').prop({
                'disabled': false,
            });
        } else {
            $('#sendPoll').prop({
                'disabled': true,
            });
        }
    });

    // С 3 шага переход на 2 шаг
    body.on('click', '#backToStep2', function (el) {
        ajaxStepFrom3To2(el);
    });

    function ajaxStepFrom3To2(el) {
        let checkedInterviewed = [];
        $('input[name=participants]:checked').each(function (key, elem) {
            checkedInterviewed.push($(elem).attr('data-participant-id'));
        });
        $.ajax({
            url: 'step/2/from/3/',
            type: 'post',
            data: {
                pollId: pollId,
                csrfmiddlewaretoken: csrf,
                checkedInterviewed: checkedInterviewed,
            },
            beforeSend: function () {
                // $(el.target).prop({
                //     'disabled': true,
                // });
                menu.addClass('disabled');
                editor.addClass('disabled');
            },
            success: function (response) {
                let headMain = $('.head__main');
                headMain.empty();
                headMain[0].insertAdjacentHTML('afterbegin', response.headMain);

                let headMove = $('.head__move');
                headMove.empty();
                headMove[0].insertAdjacentHTML('afterbegin', response.headMove);

                let categories = $('.categories-block');
                categories.empty();
                categories[0].insertAdjacentHTML('afterbegin', response.categories);

                editor.attr({
                    'data-step': '2',
                });

                menu.eq(2).removeClass('item--active');
                menu.eq(1).addClass('item--active');
            },
            complete: function () {
                // $(el.target).prop({
                //     'disabled': false,
                // });
                menu.eq(0).removeClass('disabled');
                menu.eq(1).removeClass('disabled');
                if (accessStep3) {
                    menu.eq(2).removeClass('disabled');
                }
                editor.removeClass('disabled');
            },
        });
    }

    // 3 шаг - отправка опроса
    body.on('click', '#sendPoll', function (el) {
        let checkedInterviewed = [];
        $('input[name=participants]:checked').each(function (key, elem) {
            checkedInterviewed.push($(elem).attr('data-participant-id'));
        });
        $.ajax({
            url: 'send/',
            type: 'post',
            data: {
                pollId: pollId,
                csrfmiddlewaretoken: csrf,
                checkedInterviewed: checkedInterviewed,
            },
            beforeSend: function () {
                menu.addClass('disabled');
                editor.addClass('disabled');
                // $(el.target).prop({
                //     'disabled': true,
                // });
            },
            success: function () {
                location.href = 'polls/';
            },
            error: function () {
                editor.removeClass('disabled');
                // $(el.target).prop({
                //     'disabled': false,
                // });
            }
        })
    });

    body.on('click', '.item__link', function (el) {
        let li = $(this).parent();
        let nextStep = li.attr('data-step');
        let currentStep = editor.attr('data-step');
        console.log(currentStep, nextStep)
        if (!li.hasClass('item--active') && nextStep !== currentStep) {
            if (currentStep === '1' && nextStep === '2') {
                ajaxStepFrom1To2();
            } else if (currentStep === '1' && nextStep === '3') {
                ajaxStepFrom1To3();
            } else if (currentStep === '2' && nextStep === '1') {
                ajaxStepFrom2To1();
            } else if (currentStep === '2' && nextStep === '3') {
                ajaxStepFrom2To3();
            } else if (currentStep === '3' && nextStep === '1') {
                ajaxStepFrom3To1();
            } else if (currentStep === '3' && nextStep === '2') {
                ajaxStepFrom3To2();
            } else {
                throw new Error('Unexpected attribute when going to another step');
            }
        }
    });

    function ajaxStepFrom3To1(el) {
        let checkedInterviewed = [];
        $('input[name=participants]:checked').each(function (key, elem) {
            checkedInterviewed.push($(elem).attr('data-participant-id'));
        });
        $.ajax({
            url: 'step/1/from/3/',
            type: 'post',
            data: {
                pollId: pollId,
                csrfmiddlewaretoken: csrf,
                checkedInterviewed: checkedInterviewed,
            },
            beforeSend: function () {
                // $(el.target).prop({
                //     'disabled': true,
                // });
                menu.addClass('disabled');
                editor.addClass('disabled');
            },
            success: function (response) {
                let headMain = $('.head__main');
                headMain.empty();
                headMain[0].insertAdjacentHTML('afterbegin', response.headMain);

                let headMove = $('.head__move');
                headMove.empty();
                headMove[0].insertAdjacentHTML('afterbegin', response.headMove);

                let categories = $('.categories-block');
                categories.empty();
                categories[0].insertAdjacentHTML('afterbegin', response.categories);

                editor.attr({
                    'data-step': '1',
                });

                menu.eq(2).removeClass('item--active');
                menu.eq(1).addClass('item--active');
            },
            complete: function () {
                // $(el.target).prop({
                //     'disabled': false,
                // });
                menu.eq(0).removeClass('disabled');
                menu.eq(1).removeClass('disabled');
                if (accessStep3) {
                    menu.eq(2).removeClass('disabled');
                }
                editor.removeClass('disabled');
            },
        });
    }

    function ajaxStepFrom1To3(el) {
        let template = getTemplate();
        console.log(template)
        $.ajax({
            url: 'step/3/from/1/',
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
                pollId: pollId,
                template: template,
            },
            beforeSend: function () {
                // $(el.target).prop({
                //     'disabled': true,
                // });
                editor.addClass('disabled');
                menu.addClass('disabled');
            },
            success: function (response) {
                document.documentElement.style.setProperty('--mdc-theme-primary', '#FF1841');
                document.documentElement.style.setProperty('--mdc-theme-secondary', '#FF1841');
                document.documentElement.style.setProperty('--mdc-theme-text-primary-on-dark', 'white');

                let headMain = $('.head__main');
                headMain.empty();
                headMain[0].insertAdjacentHTML('afterbegin', response.headMain);

                let headMove = $('.head__move');
                headMove.empty();
                headMove[0].insertAdjacentHTML('afterbegin', response.headMove);

                let categories = $('.categories-block');
                categories.empty();
                categories[0].insertAdjacentHTML('afterbegin', response.categories);

                editor.attr({
                    'data-step': '3',
                });

                menu.eq(0).removeClass('item--active');
                menu.eq(1).addClass('item--active');
            },
            complete: function () {
                // $(el.target).prop({
                //     'disabled': false,
                // });
                editor.removeClass('disabled');
                menu.eq(1).removeClass('disabled');
                menu.eq(0).removeClass('disabled');
                if (accessStep3) {
                    menu.eq(2).removeClass('disabled');
                }
            },
            error: function () {
            },
        });
    }

    // Автоувеличение полей ввода
    function countLines(el, delta) {
        el.style.height = '1px';
        el.style.height = (el.scrollHeight + delta) + 'px';
    }

    // Первый запуск
    function run() {
        listKeys = [];
        let questions = $('.question');

        // Кнопка далее
        if (questions.length === 0) {
            $('#nextToStep2').prop({
                'disabled': true,
            });
            menu.eq(1).addClass('disabled');
        } else {
            $('#nextToStep2').prop({
                'disabled': false,
            });
            menu.eq(1).removeClass('disabled');
        }
        if (accessStep3) {
            menu.eq(2).removeClass('disabled');
        } else {
            menu.eq(2).addClass('disabled');
        }

        // Изменение цвета
        let currentColor = $('.color__variable--select');
        let pollHeader = $('.poll-editor__header');
        pollHeader.removeClass('red blue purple');
        if (currentColor.hasClass('blue')) {
            pollHeader.addClass('blue');
            document.documentElement.style.setProperty('--mdc-theme-primary', '#001AFF');
            document.documentElement.style.setProperty('--mdc-theme-secondary', '#001AFF');
            document.documentElement.style.setProperty('--mdc-theme-text-primary-on-dark', 'white');
        } else if (currentColor.hasClass('red')) {
            pollHeader.addClass('red');
            document.documentElement.style.setProperty('--mdc-theme-primary', '#FF1841');
            document.documentElement.style.setProperty('--mdc-theme-secondary', '#FF1841');
            document.documentElement.style.setProperty('--mdc-theme-text-primary-on-dark', 'white');
        } else if (currentColor.hasClass('purple')) {
            pollHeader.addClass('purple');
            document.documentElement.style.setProperty('--mdc-theme-primary', '#DB00FF');
            document.documentElement.style.setProperty('--mdc-theme-secondary', '#DB00FF');
            document.documentElement.style.setProperty('--mdc-theme-text-primary-on-dark', 'white');
        } else {
            document.documentElement.style.setProperty('--mdc-theme-primary', '#C4C4C4');
            document.documentElement.style.setProperty('--mdc-theme-secondary', '#C4C4C4');
            document.documentElement.style.setProperty('--mdc-theme-text-primary-on-dark', 'black');
        }

        // Увеличение полей
        $('.textarea-line').each(function (key, el) {
            if (el.value !== '') {
                countLines(el, 5);
            }
        });
        $('.textarea-border').each(function (key, el) {
            if (el.value !== '') {
                countLines(el, -1);
            }
        });

        questions.each(function (key, el) {
            // Инициализация типа вопроса
            selectDeclaration(el);
            // Инициализация слайдеров
            if ($(el).attr('data-question-type') === 'range') {
                sliderDeclaration(el);
            }
            // Заносим в listKeys
            listKeys.push($(el).attr('data-question-id'))
        });
        // console.log(listQuestions)
    }

    // Создание нового опроса
    function createNewQuestion() {
        let question = document.createElement('div');
        question.classList.add('question', 'rounded-block');
        let id = checkId(createId());

        $(question).attr({
            'data-question-type': 'radio',
            'data-question-id': id,
        });

        let qMain = document.createElement('div');
        qMain.classList.add('question__main');
        question.append(qMain);

        let qName = document.createElement('textarea');
        qName.classList.add('question__name', 'textarea-border');
        $(qName).attr({
            'placeholder': 'Вопрос',
            'maxlength': maxLengthInput,
        });
        qMain.append(qName);

        let qType = document.createElement('div');
        qType.classList.add('question__type', 'unselectable');
        qMain.append(qType);

        let selectorType = '<div class="mdc-select mdc-select--outlined width-264">\n' +
            '                        <div class="mdc-select__anchor height-50" aria-labelledby="outlined-select-label">\n' +
            '                            <span id="" class="mdc-select__selected-text"></span>\n' +
            '                            <span class="mdc-select__dropdown-icon">\n' +
            '                                <svg class="mdc-select__dropdown-icon-graphic" viewBox="7 10 10 5">\n' +
            '                                    <polygon\n' +
            '                                            class="mdc-select__dropdown-icon-inactive"\n' +
            '                                            stroke="none"\n' +
            '                                            fill-rule="evenodd"\n' +
            '                                            points="7 10 12 15 17 10">\n' +
            '                                    </polygon>\n' +
            '                                    <polygon\n' +
            '                                            class="mdc-select__dropdown-icon-active"\n' +
            '                                            stroke="none"\n' +
            '                                            fill-rule="evenodd"\n' +
            '                                            points="7 15 12 10 17 15">\n' +
            '                                    </polygon>\n' +
            '                                </svg>\n' +
            '                            </span>\n' +
            '                            <span class="mdc-notched-outline">\n' +
            '                            <span class="mdc-notched-outline__leading"></span>\n' +
            '                            <span class="mdc-notched-outline__notch">\n' +
            '                            </span>\n' +
            '                            <span class="mdc-notched-outline__trailing"></span>\n' +
            '                        </span>\n' +
            '                        </div>\n' +
            '                        <div class="mdc-select__menu mdc-menu mdc-menu-surface width-264">\n' +
            '                            <ul class="mdc-list">\n' +
            '                                <li class="mdc-list-item mdc-list-item--selected" data-value="radio">\n' +
            '                                    <span class="mdc-list-item__ripple"></span>\n' +
            '                                    <span class="mdc-list-item__text">Один из списка</span>\n' +
            '                                </li>\n' +
            '                                <li class="mdc-list-item" data-value="checkbox">\n' +
            '                                    <span class="mdc-list-item__ripple"></span>\n' +
            '                                    <span class="mdc-list-item__text">Несколько из списка</span>\n' +
            '                                </li>\n' +
            '                                <li class="mdc-list-item" data-value="openQuestion">\n' +
            '                                    <span class="mdc-list-item__ripple"></span>\n' +
            '                                    <span class="mdc-list-item__text">Развёрнутый ответ</span>\n' +
            '                                </li>\n' +
            '                                <li class="mdc-list-item" data-value="range">\n' +
            '                                    <span class="mdc-list-item__ripple"></span>\n' +
            '                                    <span class="mdc-list-item__text">Шкала</span>\n' +
            '                                </li>\n' +
            '                            </ul>\n' +
            '                        </div>\n' +
            '                    </div>';
        qType.insertAdjacentHTML('afterbegin', selectorType);
        selectDeclaration(question);

        let qAnswers = document.createElement('div');
        qAnswers.classList.add('question__answers');
        question.append(qAnswers);

        let answer = document.createElement('div');
        answer.classList.add('answer');
        qAnswers.append(answer);

        let aIcon = document.createElement('div');
        aIcon.classList.add('answer__icon');
        answer.append(aIcon);

        let icon = '<div class="mdc-form-field">\n' +
            '                            <div class="mdc-radio mdc-radio--disabled">\n' +
            '                                <input class="mdc-radio__native-control" type="radio" id="" name="" disabled>\n' +
            '                                <div class="mdc-radio__background">\n' +
            '                                    <div class="mdc-radio__outer-circle"></div>\n' +
            '                                    <div class="mdc-radio__inner-circle"></div>\n' +
            '                                </div>\n' +
            '                                <div class="mdc-radio__ripple"></div>\n' +
            '                            </div>\n' +
            '                        </div>';
        aIcon.insertAdjacentHTML('afterbegin', icon);

        let aText = document.createElement('textarea');
        aText.classList.add('textarea-line', 'answer__text');
        $(aText).attr({
            'name': '',
            'id': '',
            'rows': '1',
            'placeholder': 'Вариант ответа',
            'maxlength': maxLengthInput,
        });
        answer.append(aText);

        let aClear = document.createElement('img');
        aClear.classList.add('answer__clear');
        $(aClear).attr({
            'src': '/static/main/images/icon/clear-24px.svg',
            'alt': '',
        });
        answer.append(aClear);

        let aAdd = document.createElement('a');
        aAdd.classList.add('new-answer__btn');
        aAdd.text = 'Добавить ещё вариант ответа';
        question.append(aAdd);

        let qFooter = document.createElement('div');
        qFooter.classList.add('question__footer');
        question.append(qFooter);

        let qUrn = document.createElement('img');
        qUrn.classList.add('question__urn');
        $(qUrn).attr({
            'src': '/static/main/images/icon/delete_forever-24px.svg',
            'alt': '',
        });
        qFooter.append(qUrn);

        return question;
    }

    function createNewAnswer(type) {
        let answer = document.createElement('div');
        answer.classList.add('answer');

        let aIcon = document.createElement('div');
        aIcon.classList.add('answer__icon');
        answer.append(aIcon);

        let icon;
        if (type === 'radio') {
            icon = '<div class="mdc-form-field">\n' +
                '                            <div class="mdc-radio mdc-radio--disabled">\n' +
                '                                <input class="mdc-radio__native-control" type="radio" id="" name="" disabled>\n' +
                '                                <div class="mdc-radio__background">\n' +
                '                                    <div class="mdc-radio__outer-circle"></div>\n' +
                '                                    <div class="mdc-radio__inner-circle"></div>\n' +
                '                                </div>\n' +
                '                                <div class="mdc-radio__ripple"></div>\n' +
                '                            </div>\n' +
                '                        </div>';
        } else if (type === 'checkbox') {
            icon = '<div class="mdc-form-field">\n' +
                '                            <div class="mdc-checkbox mdc-checkbox--disabled">\n' +
                '                                <input class="mdc-checkbox__native-control" type="checkbox" id="" name="" disabled>\n' +
                '                                <div class="mdc-checkbox__background">\n' +
                '                                    <div class="mdc-checkbox__outer-circle"></div>\n' +
                '                                    <div class="mdc-checkbox__inner-circle"></div>\n' +
                '                                </div>\n' +
                '                                <div class="mdc-checkbox__ripple"></div>\n' +
                '                            </div>\n' +
                '                        </div>';
        } else {
            throw new Error('Unexpected attribute when adding answer option');
        }
        aIcon.insertAdjacentHTML('afterbegin', icon);

        let aText = document.createElement('textarea');
        aText.classList.add('textarea-line', 'answer__text');
        $(aText).attr({
            'name': '',
            'id': '',
            'rows': '1',
            'placeholder': 'Вариант ответа',
            'maxlength': maxLengthInput,
        });
        answer.append(aText);

        let aClear = document.createElement('img');
        aClear.classList.add('answer__clear');
        $(aClear).attr({
            'src': '/static/main/images/icon/clear-24px.svg',
            'alt': '',
        });
        answer.append(aClear);

        return answer;
    }

    // Получить последний ключ в объекте
    function getLastKey(obg) {
        let keys = Object.keys(obg);
        return keys[keys.length - 1];
    }

    function selectDeclaration(el) {
        let sortable = new mdc.select.MDCSelect(el.querySelector('.mdc-select'));
        sortable.listen('MDCSelect:change', () => {
            let question = $(el);
            let idQuestion = question.attr('data-question-id');
            let lastVal = question.attr('data-question-type');
            let currentVal = sortable.value;
            if (lastVal !== currentVal) {
                // console.log(lastVal, currentVal)

                let answers = question.children('.question__answers');
                let newIcon;
                if (currentVal === 'checkbox') {
                    newIcon = '<div class="mdc-form-field">\n' +
                        '                            <div class="mdc-checkbox mdc-checkbox--disabled">\n' +
                        '                                <input class="mdc-checkbox__native-control" type="checkbox" id="" name="" disabled>\n' +
                        '                                <div class="mdc-checkbox__background">\n' +
                        '                                    <div class="mdc-checkbox__outer-circle"></div>\n' +
                        '                                    <div class="mdc-checkbox__inner-circle"></div>\n' +
                        '                                </div>\n' +
                        '                                <div class="mdc-checkbox__ripple"></div>\n' +
                        '                            </div>\n' +
                        '                        </div>';
                } else if (currentVal === 'radio') {
                    newIcon = '<div class="mdc-form-field">\n' +
                        '                            <div class="mdc-radio mdc-radio--disabled">\n' +
                        '                                <input class="mdc-radio__native-control" type="radio" id="" name="" disabled>\n' +
                        '                                <div class="mdc-radio__background">\n' +
                        '                                    <div class="mdc-radio__outer-circle"></div>\n' +
                        '                                    <div class="mdc-radio__inner-circle"></div>\n' +
                        '                                </div>\n' +
                        '                                <div class="mdc-radio__ripple"></div>\n' +
                        '                            </div>\n' +
                        '                        </div>';
                }
                // console.log(answers)
                question.attr({
                    'data-question-type': currentVal,
                });
                if ((lastVal === 'radio' && currentVal === 'checkbox') ||
                    (lastVal === 'checkbox' && currentVal === 'radio')) {
                    $(answers.children('.answer')).each(function (key, el) {
                        let icon = $(el).children('.answer__icon');
                        icon.empty();
                        icon[0].insertAdjacentHTML('afterbegin', newIcon);
                    });
                } else {
                    answers.empty();
                    if (currentVal === 'radio' || currentVal === 'checkbox') {
                        let answer = document.createElement('div');
                        answer.classList.add('answer');
                        answers.append(answer);

                        let aIcon = document.createElement('div');
                        aIcon.classList.add('answer__icon');
                        answer.append(aIcon);

                        aIcon.insertAdjacentHTML('afterbegin', newIcon);

                        let aText = document.createElement('textarea');
                        aText.classList.add('textarea-line', 'answer__text');
                        $(aText).attr({
                            'name': '',
                            'id': '',
                            'rows': '1',
                            'placeholder': 'Вариант ответа',
                            'maxlength': maxLengthInput,
                        });
                        answer.append(aText);

                        let aClear = document.createElement('img');
                        aClear.classList.add('answer__clear');
                        $(aClear).attr({
                            'src': '/static/main/images/icon/clear-24px.svg',
                            'alt': '',
                        });
                        answer.append(aClear);

                        let aAdd = document.createElement('a');
                        aAdd.classList.add('new-answer__btn');
                        aAdd.text = 'Добавить ещё вариант ответа';
                        answers.after(aAdd);
                    } else if (currentVal === 'openQuestion') {
                        question.children('.new-answer__btn').remove();

                        let answer = document.createElement('textarea');
                        answer.classList.add('open-question', 'textarea-line');
                        $(answer).attr({
                            'placeholder': 'Поле для ответа',
                        });
                        $(answer).prop({
                            'disabled': true,
                        });
                        answers.append(answer);
                    } else if (currentVal === 'range') {
                        question.children('.new-answer__btn').remove();
                        let answer = document.createElement('div');
                        answer.classList.add('slider-range');
                        answers.append(answer);

                        let slider = '<div class="mdc-slider mdc-slider--discrete" tabindex="0" role="slider"\n' +
                            '                         aria-valuemin="0" aria-valuemax="10" aria-valuenow="0" data-step="1"\n' +
                            '                         aria-label="Select Value" aria-disabled="false">\n' +
                            '                        <div class="mdc-slider__track-container">\n' +
                            '                            <div class="mdc-slider__track"></div>\n' +
                            '                        </div>\n' +
                            '                        <div class="mdc-slider__thumb-container">\n' +
                            '                            <div class="mdc-slider__pin">\n' +
                            '                                <span class="mdc-slider__pin-value-marker"></span>\n' +
                            '                            </div>\n' +
                            '                            <svg class="mdc-slider__thumb" width="21" height="21">\n' +
                            '                                <circle cx="10.5" cy="10.5" r="7.875"></circle>\n' +
                            '                            </svg>\n' +
                            '                            <div class="mdc-slider__focus-ring"></div>\n' +
                            '                        </div>\n' +
                            '                    </div>';
                        answer.insertAdjacentHTML('afterbegin', slider);

                        let sSetting = document.createElement('div');
                        sSetting.classList.add('slider-range__settings');
                        answer.append(sSetting);

                        let min = document.createElement('div');
                        min.classList.add('min');
                        sSetting.append(min);

                        let minLabel = document.createElement('label');
                        minLabel.classList.add('min__label');
                        $(minLabel).attr({
                            'for': `min_${idQuestion}`,
                        });
                        minLabel.textContent = 'От';
                        min.append(minLabel);

                        let minInput = document.createElement('input');
                        minInput.classList.add('input-transparent', 'slider-range__min');
                        $(minInput).attr({
                            'type': 'number',
                            'id': `min_${idQuestion}`,
                            'min': '0',
                            'max': '100',
                            'value': '0',
                        });
                        min.append(minInput);

                        let step = document.createElement('div');
                        step.classList.add('step');
                        sSetting.append(step);

                        let stepLabel = document.createElement('label');
                        stepLabel.classList.add('step__label');
                        $(stepLabel).attr({
                            'for': `step_${idQuestion}`,
                        });
                        stepLabel.textContent = 'С шагом';
                        step.append(stepLabel);

                        let stepInput = document.createElement('input');
                        stepInput.classList.add('input-transparent', 'slider-range__step');
                        $(stepInput).attr({
                            'type': 'number',
                            'id': `step_${idQuestion}`,
                            'min': '1',
                            'max': '50',
                            'value': '1',
                        });
                        step.append(stepInput);

                        let max = document.createElement('div');
                        max.classList.add('max');
                        sSetting.append(max);

                        let maxLabel = document.createElement('label');
                        maxLabel.classList.add('max__label');
                        $(maxLabel).attr({
                            'for': `max_${idQuestion}`,
                        });
                        maxLabel.textContent = 'До';
                        max.append(maxLabel);

                        let maxInput = document.createElement('input');
                        maxInput.classList.add('input-transparent', 'slider-range__max');
                        $(maxInput).attr({
                            'type': 'number',
                            'id': `max_${idQuestion}`,
                            'min': '1',
                            'max': '100',
                            'value': '10',
                        });
                        max.append(maxInput);
                        sliderDeclaration(el);
                    } else {
                        throw new Error('Unexpected attribute on question change');
                    }
                }
                // console.log(currentVal)
            }
        });
    }

    function sliderDeclaration(el) {
        let slider = new mdc.slider.MDCSlider(el.querySelector('.mdc-slider'));
        slider.min = parseInt($(el).find('.slider-range__min').val());
        slider.max = parseInt($(el).find('.slider-range__max').val());
        slider.step = parseInt($(el).find('.slider-range__step').val());
        slider.listen('MDCSlider:change', () => {
            console.log(`Value changed to ${slider.value}`);
        });
    }

    function checkId(id) {
        for (let e in listKeys) {
            if (e === id) {
                id = checkId(createId());
                break;
            }
        }
        return id;
    }

    function createId() {
        let result = "";
        let possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        for (let i = 0; i < 33; i++)
            result += possible.charAt(Math.floor(Math.random() * possible.length));
        return result;
    }

    function getTemplate() {
        let questions = $('.question');
        let template = {
            pollId: pollId,
            name: $('.poll__name').val(),
            description: $('.poll__description').val(),
            questions: [],
            color: $('.color__variable--select').attr('data-color'),
            countQuestion: questions.length,
        };
        questions.each(function (key, el) {
            let type = $(el).attr('data-question-type');
            let answersBlock = $(el).children('.question__answers');
            template.questions.push({
                id: $(el).attr('data-question-id'),
                serialNumber: key + 1,
                type: type,
                name: $(el).children('.question__main').children('.question__name ').val(),
                // answers: [],
                // countAnswers: answers.length,
                // settingsSlider: {}
            });
            if (type === 'radio' || type === 'checkbox') {
                let answers = answersBlock.children('.answer');
                template.questions[key].answers = [];
                template.questions[key].countAnswers = answers.length;
                $(answers).each(function (keyA, elA) {
                    let answerText = $(elA).children('.answer__text').val();
                    template.questions[key].answers.push(answerText);
                })
            } else if (type === 'range') {
                let settings = answersBlock.children('.slider-range').children('.slider-range__settings');
                template.questions[key].settingsSlider = {
                    min: settings.children('.min').children('.slider-range__min').val(),
                    max: settings.children('.max').children('.slider-range__max').val(),
                    step: settings.children('.step').children('.slider-range__step').val(),
                }
            } else if (type === 'openQuestion') {

            } else {
                throw new Error('unexpected attribute when receiving a poll');
            }
        });
        return template;
    }
});
