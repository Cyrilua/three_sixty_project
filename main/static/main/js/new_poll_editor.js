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
    let templateId;

    let selectedInterviewed = 0;
    let selectedTarget = false;

    // Список id кому отправляется опрос
    let interviewed;

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
                $('.taking-poll').attr({
                    'data-color': 'red',
                });
                document.documentElement.style.setProperty('--mdc-theme-primary', '#FF1841');
                document.documentElement.style.setProperty('--mdc-theme-secondary', '#FF1841');
                document.documentElement.style.setProperty('--mdc-theme-text-primary-on-dark', 'white');
            } else if (color === 'blue') {
                $('.taking-poll').attr({
                    'data-color': 'blue',
                });
                document.documentElement.style.setProperty('--mdc-theme-primary', '#001AFF');
                document.documentElement.style.setProperty('--mdc-theme-secondary', '#001AFF');
                document.documentElement.style.setProperty('--mdc-theme-text-primary-on-dark', 'white');
            } else if (color === 'purple') {
                $('.taking-poll').attr({
                    'data-color': 'purple',
                });
                document.documentElement.style.setProperty('--mdc-theme-primary', '#DB00FF');
                document.documentElement.style.setProperty('--mdc-theme-secondary', '#DB00FF');
                document.documentElement.style.setProperty('--mdc-theme-text-primary-on-dark', 'white');
            } else {
                throw new Error('Unexpected attribute on color change');
            }
        } else {
            $('.taking-poll').attr({
                'data-color': 'grey',
            });
            document.documentElement.style.setProperty('--mdc-theme-primary', '#C4C4C4');
            document.documentElement.style.setProperty('--mdc-theme-secondary', '#C4C4C4');
            document.documentElement.style.setProperty('--mdc-theme-text-primary-on-dark', 'black');
        }
    });


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
            // console.log(editor.attr('data-master'))
            if (editor.attr('data-master') !== 'true') {
                $('#nextToStep3NotMaster').prop({
                    'disabled': true,
                });
            }
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
        if (editor.attr('data-master') !== 'true') {
            $('#nextToStep3NotMaster').prop({
                'disabled': false,
            });
        }
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

    // Отмена создания
    body.on('click', '#cancel', function () {
        ajaxCancel();
    });

    function ajaxCancel() {
        $.ajax({
            url: 'cancel/',
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
                pollId: pollId,
            },
            beforeSend: function () {
                menu.addClass('disabled');
                editor.addClass('disabled');
            },
            success: function () {
                window.onunload = function () {
                    return false;
                };
                window.onbeforeunload = function () {
                    return false;
                };
                location.href = '/polls/';
            },
            complete: function () {
                menu.removeClass('disabled');
                editor.removeClass('disabled');
            }
        });
    }

    // Сохранения шаблона
    body.on('click', '#saveAs', function () {
        ajaxSaveAs(this);
    });

    function ajaxSaveAs(el) {
        let status = $(el).parent().children('.save__status');
        let data;
        let category = $('.active-sort').attr('data-part-url');
        if (category === 'preview') {
            data = {
                csrfmiddlewaretoken: csrf,
                pollId: pollId,
                templateId: templateId,
                category: 'preview',
            }
        } else if (category === 'editor') {
            let template = getTemplate();
            // console.log(template)
            data = {
                csrfmiddlewaretoken: csrf,
                pollId: pollId,
                templateId: templateId,
                category: 'editor',
                template: template,
            }
        }
        $.ajax({
            url: 'save_as/',
            type: 'post',
            data: data,
            beforeSend: function () {
                menu.addClass('disabled');
                editor.addClass('disabled');
                status.removeClass('status--loading status--error status--done')
                    .addClass('status--loading');
            },
            success: function (response) {
                if (!templateId) {
                    templateId = response.templateId;
                }
                Snackbar.show({
                    text: 'Шаблон успешно создан',
                    textColor: '#1ecb00',
                    customClass: 'custom center',
                    showAction: false,
                    duration: 3000,
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
                    actionTextColor: '#5699FF',
                    customClass: 'custom center',
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
                menu.eq(0).removeClass('disabled');
                menu.eq(1).removeClass('disabled');
                if (accessStep3) {
                    menu.eq(2).removeClass('disabled');
                }
                editor.removeClass('disabled');
                status.removeClass('status--loading status--error status--done')
            }
        });
    }

    // body.on('focusout', '.question', function () {
    //     console.log('focusout')
    // })

    // С 1 шага на 2
    body.on('click', '#nextToStep2', function (el) {
        ajaxStepFrom1To2(el);
    });

    function ajaxStepFrom1To2(el) {
        // let id = editor.attr('data-poll-id');
        let data;
        let category = $('.active-sort').attr('data-part-url');
        // let step = editor.attr('data-step');
        if (category === 'preview') {
            data = {
                csrfmiddlewaretoken: csrf,
                pollId: pollId,
                category: 'preview',
            }
        } else if (category === 'editor') {
            let template = getTemplate();
            // console.log(template)
            data = {
                csrfmiddlewaretoken: csrf,
                pollId: pollId,
                templateId: templateId,
                category: 'editor',
                template: template,
            }
        }
        $.ajax({
            url: 'step/2/from/1/',
            type: 'post',
            data: data,
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

                let participant = $('input[type=radio][name=participants]:checked');
                if (selectedTarget || participant.parent().parent().parent().length > 0) {
                    selectedTarget = participant.attr('data-participant-id');
                    $('#nextToStep3').prop({
                        'disabled': false,
                    });
                    menu.eq(1).removeClass('disabled');
                    accessStep3 = true;
                }
                // console.log(participant)
                // participant.css({
                //     // 'order': -10000,
                //     'background-color': '#F0F1F6',
                // });

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


    // смена категорий (участники/команды)
    let timeOutId;
    body.on('click', '.category', function (el) {
        let partUrl = $(this).attr('data-part-url');
        let updater = $('.loader-round');
        let loader = $('.loader__status');
        let substrate = $('.substrate');
        let search = $('.input__search');
        let step = editor.attr('data-step');
        let target = this;
        // if (step !== '2' && step !== '3') {
        //     return;
        // }
        if ($('.active-sort').attr('data-part-url') === partUrl) {
            return;
        }
        let data;
        if (step === '2') {
            // let checkedTarget = $('input[name^=participants]:checked').attr('data-participant-id');
            data = {
                pollId: pollId,
                csrfmiddlewaretoken: csrf,
                checkedTarget: selectedTarget,
            }
        } else if (step === '3') {
            let checkedInterviewed = [];
            for (let key in interviewed) {
                if (interviewed[key] === true) {
                    checkedInterviewed.push(key);
                }
            }
            // $('input[name^=participants]:checked').each(function (key, elem) {
            //     checkedInterviewed.push($(elem).attr('data-participant-id'));
            // });
            // checkedInterviewed = checkedInterviewed.filter((elem, index) => checkedInterviewed.indexOf(elem) === index);
            data = {
                pollId: pollId,
                csrfmiddlewaretoken: csrf,
                checkedInterviewed: checkedInterviewed,
            }
        } else if (step === '1') {
            if (partUrl === 'editor') {
                data = {
                    pollId: pollId,
                    csrfmiddlewaretoken: csrf,
                }
            } else if (partUrl === 'preview') {
                let template = getTemplate();
                data = {
                    pollId: pollId,
                    csrfmiddlewaretoken: csrf,
                    templateId: templateId,
                    template: template,
                }
            }

        } else {
            throw new Error('unexpected attribute when changing category');
        }
        $.ajax({
            url: `step/${step}/category/${partUrl}/`, // step = 1 | 2 | 3,  partUrl = (1 : editor | preview) | (2 | 3 : participants | teams)
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
                let content = $('.content');
                content.empty();
                content[0].insertAdjacentHTML('afterbegin', response.content);
                loader
                    .removeClass('status--loading status--done status--error');
                search.val('');

                if (partUrl === 'participants') {
                    search.attr({
                        'placeholder': 'Поиск по участникам...',
                        'data-mode': 'participants',
                    });
                    search.prop({
                        'disabled': false,
                    });

                    if (step === '3') {
                        selectedInterviewed = response.countSelectedInterviewed;
                        // $('.head__count-selected').text(selectedInterviewed);
                        let allParticipants = $('input[type=checkbox][name=participants]');
                        let participants = $('input[type=checkbox][name=participants]:checked').parent().parent().parent();
                        if (selectedInterviewed > 0 || participants.length > 0) {
                            $('#sendPoll').prop({
                                'disabled': false,
                            });
                            menu.eq(1).removeClass('disabled');
                            if (allParticipants.length === participants.length) {
                                $('.select__all ').addClass('all-checked');
                            }
                        }
                        $('.select__all').removeClass('hide');
                        // console.log(participants)
                        // participants.css({
                        //     // 'order': -10000,
                        //     'background-color': '#F0F1F6',
                        // });
                    }

                } else if (partUrl === 'teams') {
                    search.attr({
                        'placeholder': 'Поиск по командам...',
                        'data-mode': 'teams',
                    });
                    search.prop({
                        'disabled': false,
                    });
                    if (step === '3') {
                        selectedInterviewed = response.countSelectedInterviewed;
                        // $('.head__count-selected').text(selectedInterviewed);
                        $('.select__all').addClass('hide');
                    }
                } else if (step === '1') {
                    if (partUrl === 'preview') {
                        $('.color').addClass('hide');
                        if (pollId === undefined) {
                            pollId = response.pollId;
                        }
                        $('.question').each(function (key, el) {
                            // Инициализация слайдеров
                            if ($(el).attr('data-question-type') === 'range') {
                                sliderDeclaration(el,
                                    parseInt($(el).children('.range-answer').children('.min').text()),
                                    parseInt($(el).children('.range-answer').children('.max').text()));
                            }
                        });
                    } else if (partUrl === 'editor') {
                        $('.color').removeClass('hide');
                        run();
                    }

                } else {
                    throw new Error('unexpected attribute when changing category');
                }

                $('.active-sort').removeClass('active-sort');
                $(target).addClass('active-sort');
            },
            complete: function () {
                substrate.removeClass('disabled');
                timeOutId = setTimeout(function () {
                    loader.removeClass('status--loading status--done status--error');
                    updater.addClass('hide');
                }, 2000);
                menu.eq(0).removeClass('disabled');

                if (step === '1') {
                    if ($('.question').length > 0) {
                        menu.eq(1).removeClass('disabled');
                        if (accessStep3) {
                            menu.eq(2).removeClass('disabled');
                        }
                    }
                } else {
                    if ($('input[name^=participants]:checked').length > 0) {
                        if (step === '2') {
                            $('#nextToStep3').prop({
                                'disabled': false,
                            });
                            menu.eq(1).removeClass('disabled');
                            if (accessStep3) {
                                menu.eq(2).removeClass('disabled');
                            }
                        } else if (step === '3') {
                            if (selectedInterviewed > 0) {
                                $('#sendPoll').prop({
                                    'disabled': false,
                                });
                            }
                            menu.eq(1).removeClass('disabled');
                            menu.eq(2).removeClass('disabled');
                        }
                    } else {
                        if (step === '2') {
                            $('#nextToStep3').prop({
                                'disabled': true,
                            });
                            menu.eq(1).removeClass('disabled');
                        } else if (step === '3') {
                            if (selectedInterviewed === 0) {
                                $('#sendPoll').prop({
                                    'disabled': true,
                                });
                            }

                            menu.eq(1).removeClass('disabled');
                            menu.eq(2).removeClass('disabled');
                        }
                    }
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
    body.on('change', 'input[type=radio][name^=participants]', function () {
        // let scroll = window.pageYOffset;
        // console.log(scroll)
        // if ($('.teams').length > 0) {
        //     // $('.participant-active').each(function (key, elem) {
        //     //     $(elem).css({
        //     //         'order': 'initial',
        //     //     });
        //     // });
        //     // participant.css({
        //     //     'order': -10000,
        //     // });
        // } else {
        //     // $('.participant-active').each(function (key, elem) {
        //     //     $(elem).css({
        //     //         // 'order': 'initial',
        //     //         'background-color': '#FAFAFA',
        //     //     });
        //     // });
        //     // participant.css({
        //     //     // 'order': -10000,
        //     //     'background-color': '#F0F1F6',
        //     // });
        // }
        // window.scrollTo(0, scroll);


        // let participant = $(this).parent().parent().parent();
        // $('.participant-active').removeClass('participant-active');
        // participant.addClass('participant-active');


        let participant = $(this).parent().parent().parent();
        // console.log(participant)
        let category = $('.active-sort').attr('data-part-url');
        if (category === 'participants') {
            $('.participant-active').removeClass('participant-active');
        } else if (category === 'teams') {
            // console.log(0)
            if (!$(this).hasClass('changeEnd')) {
                // console.log(1)
                $('.participant-active')
                    .removeClass('participant-active')
                    .children('.radio').children('.mdc-radio').children('[type=radio]').prop({
                    'checked': false,
                });
                participant.addClass('participant-active');
                let radioWithThisId = $(`[data-participant-id=${$(this).attr('data-participant-id')}]`);
                // console.log(radioWithThisId.not(':checked'))
                radioWithThisId.not(':checked')
                    .addClass('changeEnd')
                    .trigger('click');
            } else {
                // console.log(2)
                $(this).removeClass('changeEnd');
                participant.addClass('participant-active');
            }
        }
        participant.addClass('participant-active');

        $('#nextToStep3').prop({
            'disabled': false,
        });
        accessStep3 = true;
        menu.eq(2).removeClass('disabled');
    });

    // С 2 шага на 3
    body.on('click', '#nextToStep3', function (el) {
        ajaxStepFrom2To3(el);
    });

    function ajaxStepFrom2To3(el) {
        let checkedTarget = $('input[name^=participants]:checked').attr('data-participant-id');
        // console.log(checkedTarget)
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

                // selectedInterviewed = response.countSelectedInterviewed;
                // $('.head__count-selected').text(selectedInterviewed);

                let headMove = $('.head__move');
                headMove.empty();
                headMove[0].insertAdjacentHTML('afterbegin', response.headMove);

                let categories = $('.categories-block');
                categories.empty();
                categories[0].insertAdjacentHTML('afterbegin', response.categories);

                editor.attr({
                    'data-step': '3',
                });

                // if ($('input[type=checkbox][name=participants]:checked').length > 0) {
                //     $('#sendPoll').prop({
                //         'disabled': false,
                //     })
                // }
                let allParticipants = $('input[type=checkbox][name=participants]');
                if (!interviewed) {
                    interviewed = {};
                    allParticipants.each(function (index, element) {
                        interviewed[`${$(element).attr('data-participant-id')}`] = $(element).prop('checked');
                    });
                    // console.log(interviewed)
                }

                getCountCheckedInterviewed();

                let participants = $('input[type=checkbox][name=participants]:checked').parent().parent().parent();
                if (selectedInterviewed > 0 || participants.length > 0) {
                    $('#sendPoll').prop({
                        'disabled': false,
                    });
                    menu.eq(1).removeClass('disabled');
                    if (allParticipants.length === participants.length) {
                        $('.select__all ').addClass('all-checked');
                    }
                }
                // console.log(participants)
                // participants.css({
                //     // 'order': -10000,
                //     'background-color': '#F0F1F6',
                // });

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

    function getCountCheckedInterviewed() {
        selectedInterviewed = 0;
        for (let key in interviewed) {
            if (interviewed[key]) selectedInterviewed++;
        }
        // console.log(selectedInterviewed)
        return selectedInterviewed;
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

        team.children('.team__up')[0].scrollIntoView(false);
        // team.children('.team__up')[0].scrollIntoView();
        // window.scrollBy(0, -221);
    });

    // Шаг 2 и 3 - Поиск по командам/участникам
    let ajaxSearch;
    body.on('input', '.input__search', function (el) {
        let sort = $('.sort');
        let content = $('.content');
        let loader = $('.loader-round');
        let loaderStatus = loader.children('.loader__status');
        let step = editor.attr('data-step');
        let input = $('.input__search').val();
        if (step !== '2' && step !== '3') {
            throw new Error('Unexpected attribute on search');
        }
        let data;
        if (step === '2') {
            data = {
                input: input,
                pollId: pollId,
                csrfmiddlewaretoken: csrf,
                mode: $(el.target).attr('data-mode'),   // mode = participant | teams
                // checkedTarget: $('input[name=participants]:checked').attr('data-participant-id'),
            }
        } else if (step === '3') {
            // let checkedInterviewed = [];
            // $('input[name=participants]:checked').each(function (key, elem) {
            //     checkedInterviewed.push($(elem).attr('data-participant-id'));
            // });
            // checkedInterviewed = checkedInterviewed.filter((elem, index) => checkedInterviewed.indexOf(elem) === index);
            data = {
                input: input,
                pollId: pollId,
                csrfmiddlewaretoken: csrf,
                mode: $(el.target).attr('data-mode'),   // mode = participant | teams
                // checkedInterviewed: checkedInterviewed,
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
                // selectedInterviewed = 0;
                // $('.head__count-selected').text(selectedInterviewed);
                menu.addClass('disabled');
            },
            complete: function (response) {
                ajaxSearch = undefined;
                sort.removeClass('disabled');
                loader.addClass('hide');
                loaderStatus
                    .removeClass('status--loading status--done status--error')
                menu.eq(0).removeClass('disabled');

                if (step === '2') {
                    // selectedTarget = response.selectedTarget;
                    menu.eq(1).removeClass('disabled');
                    if (selectedTarget) {
                        $('#nextToStep3').prop({
                            'disabled': false,
                        });
                        menu.eq(2).removeClass('disabled');
                    } else {
                        $('#nextToStep3').prop({
                            'disabled': true,
                        });
                        menu.eq(2).addClass('disabled');
                    }
                    if (selectedTarget) {
                        $(`input[name^=participants][data-participant-id=${selectedTarget}]`).each(function (index, element) {
                            if (!$(element).prop('checked')) {
                                $(element).trigger('click');
                            }
                        });
                    }
                } else if (step === '3') {
                    $(`input[name^=participants]`).each(function (index, element) {
                        if (interviewed) {
                            if (interviewed[`${$(element).attr('data-participant-id')}`] !== $(element).prop('checked')) {
                                $(element).trigger('click');
                            }
                        }
                    });
                    if ($('input[name^=participants]:checked').length > 0) {
                        // selectedInterviewed = response.countSelectedInterviewed;
                        // $('.head__count-selected').text(selectedInterviewed);
                        if (selectedInterviewed > 0) {
                            $('#sendPoll').prop({
                                'disabled': false,
                            });
                        }
                        menu.eq(1).removeClass('disabled');
                        if (accessStep3) {
                            menu.eq(2).removeClass('disabled');
                        }
                    } else {
                        // selectedInterviewed = response.countSelectedInterviewed;
                        // $('.head__count-selected').text(selectedInterviewed);
                        menu.eq(1).removeClass('disabled');
                        menu.eq(2).removeClass('disabled');

                        let allParticipants = $('input[type=checkbox][name=participants]');
                        let participants = $('input[type=checkbox][name=participants]:checked').parent().parent().parent();
                        if (selectedInterviewed > 0 || participants.length > 0) {
                            $('#sendPoll').prop({
                                'disabled': false,
                            });
                            if (allParticipants.length === participants.length) {
                                $('.select__all ').addClass('all-checked');
                            }
                        }
                    }
                }
            },
            success: function (response) {
                content[0].insertAdjacentHTML('afterbegin', response.content);
            }
        })
    });

    // 3 шаг - выбор тех, кому отправить
    body.on('change changeEnd', 'input[type=checkbox][name=participants]', function (event) {
        let category = $('.active-sort').attr('data-part-url');
        if (category === 'participants') {
            let checked = $('input[name=participants]:checked');
            let allCheckbox = $('input[name=participants]');
            if (selectedInterviewed > 0 || checked.length > 0) {
                $('#sendPoll').prop({
                    'disabled': false,
                });
            } else {
                $('#sendPoll').prop({
                    'disabled': true,
                });
            }
            if ($(this).prop('checked')) {
                interviewed[`${$(this).attr('data-participant-id')}`] = true;
                $(this).parent().parent().parent().addClass('participant-active');
            } else {
                interviewed[`${$(this).attr('data-participant-id')}`] = false;
                $(this).parent().parent().parent().removeClass('participant-active');
            }

            if (checked.length === allCheckbox.length) {
                $('.select__all').addClass('all-checked');
            } else {
                $('.select__all').removeClass('all-checked');
            }
            // console.log(getCountCheckedInterviewed())
            if (getCountCheckedInterviewed() > 0) {
                $('#sendPoll').prop({
                    'disabled': false,
                })
            } else {
                $('#sendPoll').prop({
                    'disabled': true,
                })
            }
        } else if (category === 'teams') {
            let participantBlockInTeam = $(this).parent().parent().parent().parent();
            let checkboxesInTeam = participantBlockInTeam.children('.participant').children('.checkbox');
            let checkedInTeam = checkboxesInTeam.children('.mdc-checkbox').children('input[name=participants]:checked');
            let allCheckboxInTeam = checkboxesInTeam.children('.mdc-checkbox').children('input[name=participants]');
            let allChecked = $('input[name=participants]:checked');
            if (selectedInterviewed > 0 || allChecked.length > 0) {
                $('#sendPoll').prop({
                    'disabled': false,
                });
            } else {
                $('#sendPoll').prop({
                    'disabled': true,
                });
            }
            if (checkedInTeam.length === allCheckboxInTeam.length) {
                participantBlockInTeam.parent().parent().children('.team__up').children('.team__actions')
                    .children('.team__select-all').addClass('team-checked');
            } else {
                participantBlockInTeam.parent().parent().children('.team__up').children('.team__actions')
                    .children('.team__select-all').removeClass('team-checked');
            }

            if (!$(this).hasClass('changeEnd')) {
                if ($(this).prop('checked')) {
                    interviewed[`${$(this).attr('data-participant-id')}`] = true;
                    let checkboxWithThisId = $(`[data-participant-id=${$(this).attr('data-participant-id')}]`);
                    checkboxWithThisId.not(':checked')
                        .addClass('changeEnd')
                        .trigger('click');
                } else {
                    interviewed[`${$(this).attr('data-participant-id')}`] = false;
                    let checkboxWithThisId = $(`[data-participant-id=${$(this).attr('data-participant-id')}]`);
                    checkboxWithThisId.filter(':checked')
                        .addClass('changeEnd')
                        .trigger('click');
                }

            } else {
                $(this).removeClass('changeEnd');
                // console.log(getCountCheckedInterviewed())
                if (getCountCheckedInterviewed() > 0) {
                    $('#sendPoll').prop({
                        'disabled': false,
                    })
                } else {
                    $('#sendPoll').prop({
                        'disabled': true,
                    })
                }
            }
        }
        // console.log(interviewed)
    });

    // body.on('changeEnd', 'input[type=checkbox][name=participants]', function () {
    //
    // })

    // Выбрать всех
    body.on('click', '.team__select-all', function (el) {
        if ($(this).hasClass('team-checked')) {
            let checked = $(this).closest('.team').children('.team__down').children('.participants')
                .children('.participant').children('.checkbox').children('.mdc-checkbox')
                .children('input[name=participants]');
            checked.trigger('click');
        } else {
            let noChecked = $(this).closest('.team').children('.team__down').children('.participants')
                .children('.participant').children('.checkbox').children('.mdc-checkbox')
                .children('input[name=participants]').not(':checked');
            noChecked.trigger('click');
        }
    });

    // С 3 шага переход на 2 шаг
    body.on('click', '#backToStep2', function (el) {
        ajaxStepFrom3To2(el);
    });

    function ajaxStepFrom3To2(el) {
        let checkedInterviewed = [];
        for (let key in interviewed) {
            if (interviewed[key] === true) {
                checkedInterviewed.push(key);
            }
        }
        // $('input[name=participants]:checked').each(function (key, elem) {
        //     checkedInterviewed.push($(elem).attr('data-participant-id'));
        // });
        // checkedInterviewed = checkedInterviewed.filter((elem, index) => checkedInterviewed.indexOf(elem) === index);
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

                // if ($('input[type=radio][name=participants]:checked').length > 0) {
                //     $('#nextToStep3').prop({
                //         'disabled': false,
                //     })
                // }
                // selectedTarget = response.selectedTarget;
                let participant = $('input[type=radio][name=participants]:checked').parent().parent().parent();
                if (selectedTarget || participant.length > 0) {
                    $('#nextToStep3').prop({
                        'disabled': false,
                    });
                    menu.eq(1).removeClass('disabled');
                }
                // console.log(participant)
                // participant.css({
                //     // 'order': -10000,
                //     'background-color': '#F0F1F6',
                // });

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

    // выбор цели
    body.on('click', 'input[name^=participants][type=radio]', function (event) {
        let id = $(this).attr('data-participant-id');
        selectedTarget = id;
    });

    // 3 шаг - отправка опроса
    body.on('click', '#sendPoll', function (el) {
        let checkedInterviewed = [];
        for (let key in interviewed) {
            if (interviewed[key] === true) {
                checkedInterviewed.push(key);
            }
        }
        // $('input[name=participants]:checked').each(function (key, elem) {
        //     checkedInterviewed.push($(elem).attr('data-participant-id'));
        // });
        // checkedInterviewed = checkedInterviewed.filter((elem, index) => checkedInterviewed.indexOf(elem) === index);
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
            success: function (response) {
                if (!response.error) {
                    window.onunload = function () {
                        return;
                    };
                    window.onbeforeunload = function () {
                        return;
                    };
                    location.href = '/polls/';
                } else {
                    editor.removeClass('disabled');
                    menu.removeClass('disabled');
                    Snackbar.show({
                        text: response.error,
                        textColor: '#ff0000',
                        customClass: 'custom center',
                        showAction: false,
                        duration: 3000,
                    });
                }
            },
            complete: function () {
                // $(el.target).prop({
                //     'disabled': false,
                // });
            },
            error: function () {
                Snackbar.show({
                    text: `Произошла ошибка отправке опроса`,
                    textColor: '#ff0000',
                    customClass: 'custom center',
                    showAction: false,
                    duration: 3000,
                });
            }
        })
    });

    body.on('click', '.item__link', function (el) {
        let li = $(this).parent();
        let nextStep = li.attr('data-step');
        let currentStep = editor.attr('data-step');
        // console.log(currentStep, nextStep)
        if (!li.hasClass('item--active') && nextStep !== currentStep) {
            if (editor.attr('data-master') === 'true') {
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
            } else {
                if (currentStep === '1' && nextStep === '3') {
                    ajaxStepFrom1To3NotMaster();
                } else if (currentStep === '3' && nextStep === '1') {
                    ajaxStepFrom3To1NotMaster();
                } else {
                    throw new Error('Unexpected attribute when going to another step');
                }
            }
        }
    });

    function ajaxStepFrom3To1(el) {
        let checkedInterviewed = [];
        for (let key in interviewed) {
            if (interviewed[key] === true) {
                checkedInterviewed.push(key);
            }
        }
        // $('input[name=participants]:checked').each(function (key, elem) {
        //     checkedInterviewed.push($(elem).attr('data-participant-id'));
        // });
        // checkedInterviewed = checkedInterviewed.filter((elem, index) => checkedInterviewed.indexOf(elem) === index);
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

    function ajaxStepFrom1To3(el) {
        let data;
        let category = $('.active-sort').attr('data-part-url');
        if (category === 'preview') {
            data = {
                csrfmiddlewaretoken: csrf,
                pollId: pollId,
                category: 'preview',
            }
        } else if (category === 'editor') {
            let template = getTemplate();
            // console.log(template)
            data = {
                csrfmiddlewaretoken: csrf,
                pollId: pollId,
                templateId: templateId,
                category: 'editor',
                template: template,
            }
        }
        $.ajax({
            url: 'step/3/from/1/',
            type: 'post',
            data: data,
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

                // selectedInterviewed = response.countSelectedInterviewed;
                // $('.head__count-selected').text(selectedInterviewed);

                let categories = $('.categories-block');
                categories.empty();
                categories[0].insertAdjacentHTML('afterbegin', response.categories);

                editor.attr({
                    'data-step': '3',
                });

                menu.eq(0).removeClass('item--active');
                menu.eq(2).addClass('item--active');

                let allParticipants = $('input[type=checkbox][name=participants]');

                if (!interviewed) {
                    interviewed = {};
                    allParticipants.each(function (index, element) {
                        interviewed[`${$(element).attr('data-participant-id')}`] = $(element).prop('checked');
                    });
                    // console.log(interviewed)
                }


                getCountCheckedInterviewed();

                let participants = $('input[type=checkbox][name=participants]:checked').parent().parent().parent();
                if (selectedInterviewed > 0 || participants.length > 0) {
                    $('#sendPoll').prop({
                        'disabled': false,
                    });
                    menu.eq(1).removeClass('disabled');
                    if (allParticipants.length === participants.length) {
                        $('.select__all ').addClass('all-checked');
                    }
                }
                // console.log(participants)
                // participants.css({
                //     // 'order': -10000,
                //     'background-color': '#F0F1F6',
                // });
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

    body.on('click', '#nextToStep3NotMaster', function (el) {
        ajaxStepFrom1To3NotMaster(el);
    });

    function ajaxStepFrom1To3NotMaster(el) {
        let data;
        let category = $('.active-sort').attr('data-part-url');
        // let step = editor.attr('data-step');
        if (category === 'preview') {
            data = {
                csrfmiddlewaretoken: csrf,
                pollId: pollId,
                category: 'preview',
            }
        } else if (category === 'editor') {
            let template = getTemplate();
            // console.log(template)
            data = {
                csrfmiddlewaretoken: csrf,
                pollId: pollId,
                templateId: templateId,
                category: 'editor',
                template: template,
            }
        }
        $.ajax({
            url: 'step/3/from/1/notMaster/',
            type: 'post',
            data: data,
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

                // selectedInterviewed = response.countSelectedInterviewed;
                // $('.head__count-selected').text(selectedInterviewed);

                let categories = $('.categories-block');
                categories.empty();
                categories[0].insertAdjacentHTML('afterbegin', response.categories);

                editor.attr({
                    'data-step': '3',
                });

                if (pollId === undefined) {
                    pollId = response.pollId;
                }

                menu.eq(0).removeClass('item--active');
                menu.eq(1).addClass('item--active');

                let allParticipants = $('input[type=checkbox][name=participants]');

                if (!interviewed) {
                    interviewed = {};
                    allParticipants.each(function (index, element) {
                        interviewed[`${$(element).attr('data-participant-id')}`] = $(element).prop('checked');
                    });
                    // console.log(interviewed)
                }

                getCountCheckedInterviewed();

                let participants = $('input[type=checkbox][name=participants]:checked').parent().parent().parent();
                if (selectedInterviewed > 0 || participants.length > 0) {
                    $('#sendPoll').prop({
                        'disabled': false,
                    });
                    menu.eq(1).removeClass('disabled');
                    if (allParticipants.length === participants.length) {
                        $('.select__all ').addClass('all-checked');
                    }
                }
                // console.log(participants)
                // participants.css({
                //     // 'order': -10000,
                //     'background-color': '#F0F1F6',
                // });
            },
            complete: function () {
                // $(el.target).prop({
                //     'disabled': false,
                // });
                editor.removeClass('disabled');
                menu.eq(0).removeClass('disabled');
                if (accessStep3) {
                    menu.eq(1).removeClass('disabled');
                }
            },
            error: function () {
            },
        });
    }

    body.on('click', '#backToStep1NotMaster', function (el) {
        ajaxStepFrom3To1NotMaster(el);
    });

    function ajaxStepFrom3To1NotMaster(el) {
        let checkedInterviewed = [];
        for (let key in interviewed) {
            if (interviewed[key] === true) {
                checkedInterviewed.push(key);
            }
        }
        // $('input[name=participants]:checked').each(function (key, elem) {
        //     checkedInterviewed.push($(elem).attr('data-participant-id'));
        // });
        // checkedInterviewed = checkedInterviewed.filter((elem, index) => checkedInterviewed.indexOf(elem) === index);
        $.ajax({
            url: 'step/1/from/3/notMaster/',
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
                editor.addClass('disabled');
                menu.addClass('disabled');
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
                editor.removeClass('disabled');
                menu.eq(1).removeClass('disabled');
                menu.eq(0).removeClass('disabled');
            },
            error: function () {
            },
        });
    }

    body.on('click', '.select__all', function (el) {
        if ($(this).hasClass('all-checked')) {
            $('input[type=checkbox][name=participants]').trigger('click');
        } else {
            $('input[type=checkbox][name=participants]').not(':checked').trigger('click');
        }
    });

    body.on('click', '.participant', function (event) {
        if ($(event.target).hasClass('participant') || $(event.target).hasClass('participant__photo') ||
            $(event.target).hasClass('name') || $(event.target).hasClass('positions-n-platforms') ||
            $(event.target).hasClass('info'))
            $(this).children('.radio, .checkbox').children('.mdc-radio, .mdc-checkbox').children('input').trigger('click');
    });

    body.on('click', 'input[type=checkbox][name=participants]', function (event) {
        // let counter = $('.head__count-selected');
        // let id = $(this).attr('data-participant-id');
        // let current = $(`[data-participant-id=${id}]`).map(function (index, elem) {
        //     return $(elem).prop('checked');
        // }).get();
        // let equally = true;
        // for (let i = 0; i < current.length; i++) {
        //     if (current[0] !== current[i]) {
        //         equally = false;
        //         return;
        //     }
        // }
        // if (equally) {
        //     if ($(this).prop('checked')) {
        //         counter.text(parseInt(counter.text()) + 1);
        //     } else {
        //         counter.text(parseInt(counter.text()) - 1);
        //     }
        // }
    });

    // Автоувеличение полей ввода
    function countLines(el, delta) {
        el.style.height = '1px';
        el.style.height = (el.scrollHeight + delta) + 'px';
    }

    // Первый запуск
    function run() {
        if (editor.attr('data-master') !== 'true') {
            accessStep3 = true
        }

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

        // Смена положения вопроса
        $('.questions').sortable({
            handle: '.question__move',
            items: "> .question",
            // tolerance: 'pointer',
            // revert: true,
            // scroll: false,
            opacity: 0.5,
            // containment: ".categories",
            // axis: "y",
            // cursorAt: { left: 5 }
        });

        // Изменение цвета
        let currentColor = $('.color__variable--select').attr('data-color');
        let pollHeader = $('.poll-editor__header');
        pollHeader.removeClass('red blue purple');
        if (currentColor === 'blue') {
            pollHeader.addClass('blue');
            document.documentElement.style.setProperty('--mdc-theme-primary', '#001AFF');
            document.documentElement.style.setProperty('--mdc-theme-secondary', '#001AFF');
            document.documentElement.style.setProperty('--mdc-theme-text-primary-on-dark', 'white');
        } else if (currentColor === 'red') {
            pollHeader.addClass('red');
            document.documentElement.style.setProperty('--mdc-theme-primary', '#FF1841');
            document.documentElement.style.setProperty('--mdc-theme-secondary', '#FF1841');
            document.documentElement.style.setProperty('--mdc-theme-text-primary-on-dark', 'white');
        } else if (currentColor === 'purple') {
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
                // console.log(1)
                sliderDeclaration(el);
            }
            // Заносим в listKeys
            listKeys.push($(el).attr('data-question-id'))
        });
        // console.log(listQuestions)

        let _pollId = $('.poll-editor').attr('data-poll-id');
        if (_pollId) {
            pollId = _pollId;
        }
    }

    // Создание нового вопроса
    function createNewQuestion() {
        let question = document.createElement('div');
        question.classList.add('question', 'rounded-block');
        let id = checkId(createId());

        $(question).attr({
            'data-question-type': 'radio',
            'data-question-id': id,
        });

        let qMove = document.createElement('img');
        qMove.classList.add('question__move');
        $(qMove).attr({
            'src': '/static/main/images/move.svg',
            'alt': '',
        });
        question.append(qMove);

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

    // изменение типа
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
                            '                         aria-valuemin="0" aria-valuemax="10" aria-valuenow="5" data-step="1"\n' +
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
                        $(step).prop({
                            'hidden': true,
                        });
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

    function sliderDeclaration(el, min, max) {
        let slider = new mdc.slider.MDCSlider(el.querySelector('.mdc-slider'));
        if (!min && !max) {
            slider.min = parseInt($(el).find('.slider-range__min').val());
            slider.max = parseInt($(el).find('.slider-range__max').val());
        } else {
            slider.min = min;
            slider.max = max;
        }
        slider.step = 1;
        slider.listen('MDCSlider:change', () => {
            // console.log(`Value changed to ${slider.value}`);
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
            name: getValueElement($('.poll__name'), true),
            description: getValueElement($('.poll__description')),
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
                name: getValueElement($(el).children('.question__main').children('.question__name '), true),
                // answers: [],
                // countAnswers: answers.length,
                // settingsSlider: {}
            });
            if (type === 'radio' || type === 'checkbox') {
                let answers = answersBlock.children('.answer');
                template.questions[key].answers = [];
                template.questions[key].countAnswers = answers.length;
                $(answers).each(function (keyA, elA) {
                    let answerText = getValueElement($(elA).children('.answer__text'), true);
                    let answerId = $(elA).attr('data-real-id');
                    template.questions[key].answers.push({
                        text: answerText,
                        id: answerId,
                    });
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

    /**
     * getValueElement
     *
     * @param {jquery, HTMLElement} element
     * @param {boolean} alternative
     * @returns {string}
     */
    function getValueElement(element, alternative = false) {
        let val = $(element).val();
        if (alternative && val === '') {
            val = $(element).attr('placeholder');
        }
        return val;
    }
});
