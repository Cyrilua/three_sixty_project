class ValidationError extends Error {
    constructor(message) {
        super(message);
        this.name = "ValidationError";
    }
}

const maxAnswers = 5;
const maxQuestions = 5;
const timeAnimation = 2000;

$(function () {

    // TODO Загрузка и отображение данных с сервера

    const poll_questions = $('.poll_questions');
    const body = $('body');

    // Настройка элементов сразу после загрузки
    $('.poll-head-name').height(function () {
        countLines($(this)[0], 0);
    });
    $('.poll-head-about').height(function () {
        countLines($(this)[0], 4);
    });
    $('.question-main-name').height(function () {
        countLines($(this)[0], 2);
    });
    $('.question-main-answer').height(function () {
        countLines($(this)[0], 4);
    });
    $('.question-main-answers-answer-range-settings-min, .question-main-answers-answer-range-settings-step, .question-main-answers-answer-range-settings-max').height(function () {
        $(this)[0].value = $(this)[0].value.replace(/[^\d]/g, '');
    });
    $('.question-main-answer-remove').height(function () {
        if ($(this).parent().parent().children('.question-main-answers-answer').length === 1) {
            $(this).addClass('invisible');
        }
    });
    $('.poll-head-navigation-next-page').height(function () {
        if (poll_questions.children('.question').length === 0) {
            $(this).attr({
                'disabled': true,
            });
        }
    });
    $('.question-radio').height(function () {
        let elems = $(this).children('.question-main').children('.question-main-answers').children('.question-main-answers-answer').children('.question-radio-main-answer');
        elems.css({
            display: 'inline',
        });
        elems.animate({
            opacity: '1',
        }, timeAnimation * 2)
    });
    $('.question-checkbox').height(function () {
        let elems = $(this).children('.question-main').children('.question-main-answers').children('.question-main-answers-answer').children('.question-checkbox-main-answer');
        elems.css({
            display: 'inline',
        });
        elems.animate({
            opacity: '1',
        }, timeAnimation * 2)
    });

    // Сохранить опрос в Избранных
    $('.poll_questions-navigate-save_in_favorite').click(function (event) {
        event.preventDefault();
        // TODO Сохранение в избранных
    });

    // Перейти к отправке опроса
    body.on('click', '.poll-head-navigation-next-page', function () {
        // TODO
        console.log('Отправка опроса -->')
    });

    // Удаление опроса
    body.on('click', '.poll-head-remove', function (event) {
        event.preventDefault();
        if (confirm('Вы действительно хотите удалить данный опрос?')) {
            // TODO
            alert('Удаление данного опроса');
            location.href = '/poll/';
        }
    });

    // Отмена Enter в textarea
    body.on('keydown', 'textarea', function (e) {
        if (e.keyCode === 13)
            e.preventDefault();
    });

    // Настройки для полей
    body.on('input', '.poll-head-name', function () {
        countLines($(this)[0], 0);
    });
    body.on('input', '.poll-head-about', function () {
        countLines($(this)[0], 4);
    });
    body.on('input', '.question-main-name', function () {
        countLines($(this)[0], 2);
    });
    body.on('input', '.question-main-answer', function () {
        countLines($(this)[0], 4);
    });
    body.on('input', '.question-main-answers-answer-range-settings-min, .question-main-answers-answer-range-settings-step, .question-main-answers-answer-range-settings-max', function () {
        $(this)[0].value = $(this)[0].value.replace(/[^\d]/g, '');
    });

    // Смена типа вопроса
    body.on('input', '.question-settings-type_question', function () {
        let question = $(this).parent().parent();
        let questionMain = question.children('.question-main');
        let questionMainAnswers = questionMain.children('.question-main-answers');
        let lastType;
        let currentType = $(this)[0].value;
        // Очитстка от старых классов
        if (question.hasClass('question-checkbox')) {
            question.removeClass('question-checkbox');
            lastType = 'question-checkbox';
        } else if (question.hasClass('question-range')) {
            question.removeClass('question-range');
            lastType = 'question-range';
        } else if (question.hasClass('question-open_question')) {
            question.removeClass('question-open_question');
            lastType = 'question-open_question';
        } else if (question.hasClass('question-radio')) {
            question.removeClass('question-radio');
            lastType = 'question-radio';
        } else {
            throw new ValidationError("question-settings-type_question ERROR!!!");
        }
        // Добавление новых классов
        if (currentType === 'radio') {
            question.addClass('question-radio');
        } else if (currentType === 'checkbox') {
            question.addClass('question-checkbox');
        } else if (currentType === 'range') {
            question.addClass('question-range');
        } else if (currentType === 'open_question') {
            question.addClass('question-open_question');
        } else {
            throw new ValidationError("Смена типа ERROR!!!");
        }
        // Смена типа (отображение)
        if (lastType === 'question-radio' && currentType === 'checkbox' || lastType === 'question-checkbox' && currentType === 'radio') {
            let answers = questionMainAnswers.children('.question-main-answers-answer');
            let oldElems;
            let newElems;
            if (lastType === 'question-radio' && currentType === 'checkbox') {
                oldElems = answers.children('.question-radio-main-answer');
                newElems = answers.children('.question-checkbox-main-answer');
            } else if (lastType === 'question-checkbox' && currentType === 'radio') {
                oldElems = answers.children('.question-checkbox-main-answer');
                newElems = answers.children('.question-radio-main-answer');
            }
            oldElems.animate({
                    opacity: 0,
                },
                timeAnimation,
                function () {
                    $(this).css({
                        display: 'none',
                    });
                    newElems.css({
                        display: 'inline',
                    });
                    newElems.animate({
                            opacity: 1,
                        },
                        timeAnimation,
                    );
                }
            );
        } else {
            let delta = 0;
            let height = parseFloat(question.css('height'));
            question.css({height: height});
            let btnAdd;
            if (lastType === 'question-radio' || lastType === 'question-checkbox') {
                btnAdd = questionMain.children('.question-main-add');
                btnAdd.animate({
                        opacity: 0,
                    },
                    {
                        duration: timeAnimation,
                        queue: false,
                    },
                );
            }
            delta = parseFloat(questionMain.css('height'));
            questionMainAnswers.animate({
                    opacity: 0,
                },
                {
                    duration: timeAnimation,
                    queue: false,
                    complete: function () {
                        $(this).children().remove();
                        if (lastType === 'question-radio' || lastType === 'question-checkbox')
                            btnAdd.remove();
                        if (currentType === 'radio') {
                            createRadioOrCheckbox('radio', questionMainAnswers, questionMain);
                        } else if (currentType === 'checkbox') {
                            createRadioOrCheckbox('checkbox', questionMainAnswers, questionMain);
                        } else if (currentType === 'range') {
                            createRange(questionMainAnswers);
                        } else if (currentType === 'open_question') {
                            createOpenQuestion(questionMainAnswers);
                        }
                        delta -= parseFloat(questionMain.css('height'));
                        height -= delta;
                        question.children('.question-navigate').css({top: '+=' + delta.toString()});
                        question.children('.question-navigate').animate({
                                top: '-=' + delta.toString(),
                            },
                            {
                                duration: timeAnimation,
                                queue: false,

                            },
                        );
                        question.animate({
                                height: height,
                            },
                            {
                                duration: timeAnimation,
                                queue: false,
                            },
                        );
                        $(this).animate({
                                opacity: 1,
                            },
                            {
                                duration: timeAnimation,
                                queue: false,
                                complete: function () {
                                    question.css({height: 'auto'});
                                }
                            },
                        );
                    }
                },
            );
        }
    });


    //     if ($(this)[0].value === 'radio') {
    //         question.addClass('question-radio');
    //         if (lastType === 'question-checkbox') {
    //             let answers = questionMainAnswers.children('.question-main-answers-answer');
    //             answers.children('.question-checkbox-main-answer').animate({
    //                     opacity: 0,
    //                 },
    //                 timeAnimation,
    //                 function () {
    //                     $(this).css({
    //                         display: 'none',
    //                     });
    //                     let radio = answers.children('.question-radio-main-answer');
    //                     radio.css({
    //                         display: 'inline',
    //                     });
    //                     radio.animate({
    //                             opacity: 1,
    //                         },
    //                         timeAnimation,
    //                     );
    //                 }
    //             );
    //         } else {
    //             // questionMainAnswers.children().remove();
    //             // createRadioOrCheckbox('radio', questionMainAnswers, questionMain);
    //
    //             // let height = questionMainAnswers.css('height');
    //             // questionMainAnswers.animate({
    //             //         opacity: 0,
    //             //         height: height,
    //             //     },
    //             //     timeAnimation,
    //             //     function () {
    //             //         $(this).children().remove();
    //             //         createRadioOrCheckbox('radio', questionMainAnswers, questionMain);
    //             //         height = questionMainAnswers.children().css('height');
    //             //         $(this).animate({
    //             //                 opacity: 1,
    //             //                 height: height,
    //             //             },
    //             //             timeAnimation,
    //             //             function () {
    //             //                 $(this).animate({height: 'auto'}, timeAnimation / 2, function () {
    //             //                     $(this).css({height: 'auto'});
    //             //                 });
    //             //             }
    //             //         );
    //             //     }
    //             // );
    //
    //             let height = question.css('height');
    //             question.css({height: height});
    //             // let btnAdd = questionMain.children('.question-main-add');
    //             $(questionMainAnswers).animate({
    //                     opacity: 0,
    //                 },
    //                 1000,
    //                 function () {
    //
    //                 }
    //             )
    //         }
    //     } else if ($(this)[0].value === 'checkbox') {
    //         question.addClass('question-checkbox');
    //         if (lastType === 'question-radio') {
    //             let answers = questionMainAnswers.children('.question-main-answers-answer');
    //             answers.children('.question-radio-main-answer').animate({
    //                     opacity: 0,
    //                 },
    //                 timeAnimation,
    //                 function () {
    //                     $(this).css({
    //                         display: 'none',
    //                     });
    //                     let checkbox = answers.children('.question-checkbox-main-answer');
    //                     checkbox.css({
    //                         display: 'inline',
    //                     });
    //                     checkbox.animate({
    //                             opacity: 1,
    //                         },
    //                         timeAnimation,
    //                     );
    //                 }
    //             );
    //         } else {
    //             // questionMainAnswers.children().remove();
    //             // createRadioOrCheckbox('checkbox', questionMainAnswers, questionMain);
    //
    //             let height = questionMainAnswers.css('height');
    //             questionMainAnswers.animate({
    //                     opacity: 0,
    //                     height: height,
    //                 },
    //                 timeAnimation,
    //                 function () {
    //                     $(this).children().remove();
    //                     createRadioOrCheckbox('checkbox', questionMainAnswers, questionMain);
    //                     height = questionMainAnswers.children().css('height');
    //                     $(this).animate({
    //                             opacity: 1,
    //                             height: height,
    //                         },
    //                         timeAnimation,
    //                         function () {
    //                             $(this).animate({height: 'auto'}, timeAnimation / 2, function () {
    //                                 $(this).css({height: 'auto'});
    //                             });
    //                         }
    //                     );
    //                 }
    //             );
    //         }
    //     } else if ($(this)[0].value === 'range') {
    //         question.addClass('question-range');
    //         // let height = questionMainAnswers.css('height');
    //         // questionMainAnswers.css({'opacity': 1});
    //         // $(questionMainAnswers).animate({
    //         //         opacity: 0,
    //         //         height: height,
    //         //     },
    //         //     timeAnimation,
    //         //     function () {
    //         //         $(this).children().remove();
    //         //         if (lastType === 'question-radio' || lastType === 'question-checkbox')
    //         //             questionMain.children('.question-main-add').animate({
    //         //                     opacity: 0,
    //         //                 },
    //         //                 timeAnimation,
    //         //                 function () {
    //         //                     $(this).remove();
    //         //                 }
    //         //             );
    //         //         createRange(questionMainAnswers);
    //         //         height = questionMainAnswers.children().css('height');
    //         //         $(this).animate({
    //         //                 opacity: 1,
    //         //                 height: height,
    //         //             },
    //         //             timeAnimation,
    //         //             function () {
    //         //                 $(this).animate({height: 'auto'}, timeAnimation / 2, function () {
    //         //                     $(this).css({height: 'auto'});
    //         //                 });
    //         //             }
    //         //         );
    //         //     }
    //         // );
    //
    //
    //         // questionMainAnswers.children().remove();
    //         // if (lastType === 'question-radio' || lastType === 'question-checkbox')
    //         //     questionMain.children('.question-main-add').remove();
    //         // createRange(questionMainAnswers);
    //     } else if ($(this)[0].value === 'open_question') {
    //         question.addClass('question-open_question');
    //         // let height = questionMainAnswers.css('height');
    //         // questionMainAnswers.css({'opacity': 1});
    //         // $(questionMainAnswers).animate({
    //         //         opacity: 0,
    //         //         height: height,
    //         //     },
    //         //     timeAnimation,
    //         //     function () {
    //         //         $(this).children().remove();
    //         //         if (lastType === 'question-radio' || lastType === 'question-checkbox')
    //         //             questionMain.children('.question-main-add').animate({
    //         //                     opacity: 0,
    //         //                 },
    //         //                 timeAnimation,
    //         //                 function () {
    //         //                     $(this).remove();
    //         //                 }
    //         //             );
    //         //         createOpenQuestion(questionMainAnswers);
    //         //         height = questionMainAnswers.children().css('height');
    //         //         $(this).animate({
    //         //                 opacity: 1,
    //         //                 height: height,
    //         //             },
    //         //             timeAnimation,
    //         //             function () {
    //         //                 $(this).animate({height: 'auto'}, timeAnimation / 2, function () {
    //         //                     $(this).css({height: 'auto'});
    //         //                 });
    //         //             }
    //         //         );
    //         //     }
    //         // );
    //
    //
    //         // let delta = 0;
    //         // let height = parseFloat(question.css('height'));
    //         // question.css({height: height});
    //         // let btnAdd;
    //         // if (lastType === 'question-radio' || lastType === 'question-checkbox') {
    //         //     btnAdd = questionMain.children('.question-main-add');
    //         //     btnAdd.animate({
    //         //             opacity: 0,
    //         //         },
    //         //         {
    //         //             duration: timeAnimation,
    //         //             queue: false,
    //         //         },
    //         //     );
    //         // }
    //         // delta = parseFloat(questionMain.css('height'));
    //         // questionMainAnswers.animate({
    //         //         opacity: 0,
    //         //     },
    //         //     {
    //         //         duration: timeAnimation,
    //         //         queue: false,
    //         //         complete: function () {
    //         //             $(this).children().remove();
    //         //             if (lastType === 'question-radio' || lastType === 'question-checkbox')
    //         //                 btnAdd.remove();
    //         //             createOpenQuestion(questionMainAnswers);
    //         //             delta -= parseFloat(questionMain.css('height'));
    //         //             height -= delta;
    //         //             question.children('.question-navigate').css({top: '+=' + delta.toString()})
    //         //             question.children('.question-navigate').animate({
    //         //                     top: '-=' + delta.toString(),
    //         //                 },
    //         //                 {
    //         //                     duration: timeAnimation,
    //         //                     queue: false,
    //         //                 },
    //         //             );
    //         //             question.animate({
    //         //                     height: height,
    //         //                 },
    //         //                 {
    //         //                     duration: timeAnimation,
    //         //                     queue: false,
    //         //                 },
    //         //             );
    //         //
    //         //             $(this).animate({
    //         //                     opacity: 1,
    //         //                 },
    //         //                 {
    //         //                     duration: timeAnimation,
    //         //                     queue: false,
    //         //                 },
    //         //             );
    //         //         }
    //         //     },
    //         // )
    //
    //
    //         // questionMainAnswers.children().remove();
    //         // if (lastType === 'question-radio' || lastType === 'question-checkbox')
    //         //     questionMain.children('.question-main-add').remove();
    //         // createOpenQuestion(questionMainAnswers);
    //     } else {
    //         throw new ValidationError("question-settings-type_question ERROR!!!");
    //     }
    // });

    // Добавление варианта ответа
    body.on('click', '.question-main-add', function (event) {
        event.preventDefault();
        let answers = $(this).prev('.question-main-answers');
        let type;
        let question = $(this).parent().parent();
        if (question.hasClass('question-radio')) {
            type = 'radio';
        } else if (question.hasClass('question-checkbox')) {
            type = 'checkbox';
        } else {
            throw new ValidationError("Добавление варианта ответа ERROR!!!");
        }
        // answers.css({height: height});
        createNewAnswer(type, answers);
        let allAnswers = answers.children('.question-main-answers-answer');
        let lastAnswer = allAnswers.last();
        let height = lastAnswer.css('height');
        let delta = parseFloat(answers.css('margin-bottom')) + parseFloat($(this).css('height'));
        console.log(delta)
        lastAnswer.css({
            opacity: 0,
            height: 0,
        });
        lastAnswer.animate({
            opacity: 1,
            height: height,
        }, {
            duration: timeAnimation,
            queue: false,
            complete: function () {
                lastAnswer.css({height: 'auto'});
            }
        });
        if (allAnswers.length === 2) {
            let btnRemoveAnswer = allAnswers.children('.question-main-answer-remove').first();
            btnRemoveAnswer.css({opacity: 0});
            btnRemoveAnswer.removeClass('invisible');
            btnRemoveAnswer.animate({
                    opacity: 1,
                },
                {
                    duration: timeAnimation,
                    queue: false,
                    complete: function () {
                    }
                }
            );
        }
        if (allAnswers.length === maxAnswers) {
            // TODO
            // $(this).addClass('isDisabled');
            // let heightQuestion = question.height;
            // question.css({height: heightQuestion});
            // $(this).animate({
            //     height: 0,
            //     opacity: 0,
            //     margin: 0,
            // }, {
            //     duration: timeAnimation,
            //     queue: false,
            //     complete: function () {
            //         $(this).addClass('d-none');
            //     }
            // });
            // question.animate({
            //     height: '-=' + delta.toString(),
            // }, {
            //     duration: timeAnimation,
            //     queue: false,
            //     complete: function () {
            //         question.css({height: 'auto'});
            //     }
            // });
        }
    });

    // Удаление варианта ответа
    body.on('click', '.question-main-answer-remove', function () {
        let answer = $(this).parent();
        let answers = answer.parent();
        let countAnswers = answers.children('.question-main-answers-answer').length;
        if (countAnswers > 1) {
            let currentAnswer = answer;
            let currentAnswerNumber = parseInt(currentAnswer.children('.question-main-answer').attr('placeholder').split(' ')[1]);
            if (countAnswers !== currentAnswerNumber) {
                let nextAnswer = currentAnswer.next();
                let nextAnswerInput = nextAnswer.children('.question-main-answer');
                let nextAnswerNumber = parseInt(nextAnswerInput.attr('placeholder').split(' ')[1]);
                while (nextAnswer.length !== 0) {
                    nextAnswerInput.attr({'placeholder': 'Вариант ' + currentAnswerNumber});
                    currentAnswer = nextAnswer;
                    currentAnswerNumber = nextAnswerNumber;
                    nextAnswer = nextAnswer.next();
                    if (nextAnswer.length !== 0) {
                        nextAnswerInput = nextAnswer.children('.question-main-answer');
                        nextAnswerNumber = parseInt(nextAnswerInput.attr('placeholder').split(' ')[1]);
                    }
                }
            }
            if (countAnswers === maxAnswers) {
                answers.parent().children('.question-main-add').fadeIn(timeAnimation);
            }
            answer.fadeOut(timeAnimation, function () {
                $(this).remove();
            });


            // if (countAnswers === maxAnswers) {
            //     answers.parent().children('.question-main-add').fadeIn(timeAnimation);
            // }
            // answer.fadeOut(timeAnimation, function () {
            //     $(this).remove();
            // });


            let otherAnswers = answers.children('.question-main-answers-answer');
            if (otherAnswers.length - 1 <= 1) {
                otherAnswers.children('.question-main-answer-remove').addClass('invisible');
            }
        } else {
            throw new ValidationError("Удаление варианта ответа ERROR!!!");
        }
    });

    // Удаление вопроса
    body.on('click', '.question-navigate-remove_question', function () {
        let question = $(this).parent().parent();
        let countQuestions = question.parent().children('.question').length;
        question.remove();
        if (countQuestions - 1 === 0) {
            let btnToNextStep = $('.poll-head-navigation-next-page');
            btnToNextStep.attr({
                'disabled': true,
            });
        }
        if (countQuestions === maxQuestions) {
            $('.poll_questions-navigate-add_question').attr({
                'disabled': false,
            });
        }
    });

    // Добавление вопроса
    body.on('click', '.poll_questions-navigate-add_question', function () {
        createNewQuestion(poll_questions);
        let countQuestions = $('.poll_questions').children('.question').length;
        if (countQuestions === 1) {
            $('.poll-head-navigation-next-page').attr({
                'disabled': false,
            });
        }
        if (countQuestions === maxQuestions) {
            $(this).attr({
                'disabled': true,
            });
        }
    });

    // Перемещение вопросов
    poll_questions.sortable({
        handle: '.question-move-platform',
        scroll: false,
        tolerance: 'move',
        revert: 150,
        // containment: ".poll-container_move",
        // axis: 'y'
    });
});

// Автоувеличение полей ввода
function countLines(el, delta) {
    el.style.height = '1px';
    el.style.height = (el.scrollHeight + delta) + 'px';
}

function createRadioOrCheckbox(type, questionMainAnswers, questionMain) {
    createNewAnswer(type, questionMainAnswers);
    createBtnAddAnswer(questionMain);
}

function createRange(questionMainAnswers) {
    let questionMainAnswersAnswer = document.createElement('div');
    questionMainAnswersAnswer.classList.add('question-main-answers-answer');
    let questionMainAnswersAnswerRangeBox = document.createElement('div');
    questionMainAnswersAnswerRangeBox.classList.add('question-main-answers-answer-range-box');
    let questionMainAnswersAnswerRange = document.createElement('div');
    questionMainAnswersAnswerRange.classList.add('question-main-answers-answer-range');
    let questionMainAnswersAnswerRangeSettings = document.createElement('div');
    questionMainAnswersAnswerRangeSettings.classList.add('question-main-answers-answer-range-settings');
    let questionMainAnswersAnswerRangeSettingsMin = document.createElement('input');
    questionMainAnswersAnswerRangeSettingsMin.classList.add('question-main-answers-answer-range-settings-min');
    questionMainAnswersAnswerRangeSettingsMin.type = 'text';
    questionMainAnswersAnswerRangeSettingsMin.placeholder = 'От';
    questionMainAnswersAnswerRangeSettingsMin.maxLength = 5;
    let questionMainAnswersAnswerRangeSettingsStepBox = document.createElement('div');
    questionMainAnswersAnswerRangeSettingsStepBox.classList.add('question-main-answers-answer-range-settings-step-box');
    let questionMainAnswersAnswerRangeSettingsBeforeStep = document.createElement('span');
    questionMainAnswersAnswerRangeSettingsBeforeStep.classList.add('question-main-answers-answer-range-settings-before-step');
    questionMainAnswersAnswerRangeSettingsBeforeStep.textContent = 'С шагом:';
    let questionMainAnswersAnswerRangeSettingsStep = document.createElement('input');
    questionMainAnswersAnswerRangeSettingsStep.classList.add('question-main-answers-answer-range-settings-step');
    questionMainAnswersAnswerRangeSettingsStep.type = 'text';
    questionMainAnswersAnswerRangeSettingsStep.value = '1';
    questionMainAnswersAnswerRangeSettingsStep.maxLength = 5;
    questionMainAnswersAnswerRangeSettingsStep.autocomplete = 'off';
    let questionMainAnswersAnswerRangeSettingsMax = document.createElement('input');
    questionMainAnswersAnswerRangeSettingsMax.classList.add('question-main-answers-answer-range-settings-max');
    questionMainAnswersAnswerRangeSettingsMax.type = 'text';
    questionMainAnswersAnswerRangeSettingsMax.placeholder = 'До';
    questionMainAnswersAnswerRangeSettingsMax.maxLength = 5;
    questionMainAnswersAnswerRangeSettingsStepBox.append(questionMainAnswersAnswerRangeSettingsBeforeStep, questionMainAnswersAnswerRangeSettingsStep);
    questionMainAnswersAnswerRangeSettings.append(questionMainAnswersAnswerRangeSettingsMin, questionMainAnswersAnswerRangeSettingsStepBox, questionMainAnswersAnswerRangeSettingsMax);
    questionMainAnswersAnswerRangeBox.append(questionMainAnswersAnswerRange, questionMainAnswersAnswerRangeSettings);
    questionMainAnswersAnswer.append(questionMainAnswersAnswerRangeBox);
    questionMainAnswers.append(questionMainAnswersAnswer);
}

function createOpenQuestion(questionMainAnswers) {
    let questionMainAnswersAnswer = document.createElement('div');
    questionMainAnswersAnswer.classList.add('question-main-answers-answer');
    let questionMainAnswersAnswerOpen_question = document.createElement('span');
    questionMainAnswersAnswerOpen_question.classList.add('question-main-answers-answer-open_question');
    questionMainAnswersAnswerOpen_question.textContent = 'Текстовое поле';
    questionMainAnswersAnswer.append(questionMainAnswersAnswerOpen_question);
    questionMainAnswers.append(questionMainAnswersAnswer);
}

function createBtnAddAnswer(questionMain) {
    let questionMainAdd = document.createElement('a');
    questionMainAdd.classList.add('question-main-add');
    questionMainAdd.href = '#';
    questionMainAdd.textContent = 'Добавить еще вариант';
    questionMain.append(questionMainAdd);
}

function createNewQuestion(poll_questions) {
    let question = document.createElement('div');
    let questionClassList = question.classList;
    questionClassList.add('question');
    questionClassList.add('question-radio');
    questionClassList.add('rounded-block');

    let questionMove = document.createElement('div');
    questionMove.classList.add('question-move');
    let questionMovePlatform = document.createElement('div');
    questionMovePlatform.classList.add('question-move-platform');
    let questionMovePlatformImg = document.createElement('img');
    questionMovePlatformImg.classList.add('question-move-platform-img');
    questionMovePlatformImg.alt = '';
    questionMovePlatformImg.src = '../../static/main/images/move.svg';

    questionMovePlatform.append(questionMovePlatformImg);
    questionMove.append(questionMovePlatform);

    let questionMain = document.createElement('div');
    questionMain.classList.add('question-main');
    let questionMainName = document.createElement('textarea');
    questionMainName.classList.add('question-main-name');
    questionMainName.name = '';
    questionMainName.id = '';
    questionMainName.rows = 1;
    questionMainName.placeholder = 'Вопрос';
    let questionMainAnswers = document.createElement('div');
    questionMainAnswers.classList.add('question-main-answers');

    createRadioOrCheckbox('radio', questionMainAnswers, questionMain);
    questionMain.prepend(questionMainName, questionMainAnswers);

    let questionSettings = document.createElement('div');
    questionSettings.classList.add('question-settings');
    let questionSettingsType_question = document.createElement('select');
    questionSettingsType_question.classList.add('question-settings-type_question');
    questionSettingsType_question.id = 'type_question';
    questionSettingsType_question.name = 'type_question';
    let questionSettingsType_questionOption1 = document.createElement('option');
    questionSettingsType_questionOption1.value = 'radio';
    questionSettingsType_questionOption1.classList.add('question-settings-type_question-option');
    questionSettingsType_questionOption1.selected = true;
    questionSettingsType_questionOption1.text = 'Один из списка';
    let questionSettingsType_questionOption2 = document.createElement('option');
    questionSettingsType_questionOption2.value = 'checkbox';
    questionSettingsType_questionOption2.classList.add('question-settings-type_question-option');
    questionSettingsType_questionOption2.text = 'Несколько из списка';
    let questionSettingsType_questionOption3 = document.createElement('option');
    questionSettingsType_questionOption3.value = 'range';
    questionSettingsType_questionOption3.classList.add('question-settings-type_question-option');
    questionSettingsType_questionOption3.text = 'Шкала';
    let questionSettingsType_questionOption4 = document.createElement('option');
    questionSettingsType_questionOption4.value = 'open_question';
    questionSettingsType_questionOption4.classList.add('question-settings-type_question-option');
    questionSettingsType_questionOption4.text = 'Открытый вопрос';

    questionSettingsType_question.append(questionSettingsType_questionOption1, questionSettingsType_questionOption2, questionSettingsType_questionOption3, questionSettingsType_questionOption4);
    questionSettings.append(questionSettingsType_question);

    let questionNavigate = document.createElement('div');
    let questionSettingsClassList = questionNavigate.classList;
    questionSettingsClassList.add('question-navigate');
    questionSettingsClassList.add('text-right');
    let questionNavigateRemove_question = document.createElement('button');
    questionNavigateRemove_question.classList.add('question-navigate-remove_question');
    let questionNavigateRemove_questionImg = document.createElement('img');
    questionNavigateRemove_questionImg.classList.add('question-navigate-remove_question-img');
    questionNavigateRemove_questionImg.src = '../../static/main/images/remove2.svg';
    questionNavigateRemove_questionImg.alt = '';

    questionNavigateRemove_question.append(questionNavigateRemove_questionImg);
    questionNavigate.append(questionNavigateRemove_question);

    question.append(questionMove, questionMain, questionSettings, questionNavigate);
    poll_questions.append(question);
}

function createNewAnswer(type, questionMainAnswers) {
    let answerNumber = $(questionMainAnswers).children().length;
    if (answerNumber >= maxAnswers) {
        throw new ValidationError("createNewAnswer ERROR!!!");
    }
    answerNumber++;

    let questionMainAnswersAnswer = document.createElement('div');
    questionMainAnswersAnswer.classList.add('question-main-answers-answer');
    let questionRadioMainAnswer = document.createElement('span');
    let questionCheckboxMainAnswer = document.createElement('span');
    let questionMainAnswer = document.createElement('textarea');
    questionMainAnswer.classList.add('question-main-answer');
    questionMainAnswer.name = '';
    questionMainAnswer.id = '';
    questionMainAnswer.rows = 1;
    questionMainAnswer.placeholder = 'Вариант ' + answerNumber;
    questionMainAnswer.setAttribute('data-number_answer', '1');
    let questionMainAnswerRemove = document.createElement('button');
    questionMainAnswerRemove.classList.add('question-main-answer-remove');
    if ($(questionMainAnswers).children('.question-main-answers-answer').length === 0) {
        questionMainAnswerRemove.classList.add('invisible');
    }
    let questionMainAnswerRemoveImg = document.createElement('img');
    questionMainAnswerRemoveImg.classList.add('question-main-answer-remove-img');
    questionMainAnswerRemoveImg.src = '../../static/main/images/cross.svg';
    questionMainAnswerRemoveImg.alt = '';
    if (type === 'radio') {
        questionRadioMainAnswer.classList.add('question-radio-main-answer');
        let questionCheckboxMainAnswerClassList = questionCheckboxMainAnswer.classList;
        questionCheckboxMainAnswerClassList.add('question-checkbox-main-answer');
        $(questionRadioMainAnswer).css({
            opacity: 1,
            display: 'inline',
        });
    } else if (type === 'checkbox') {
        let questionRadioMainAnswerClassList = questionRadioMainAnswer.classList;
        questionRadioMainAnswerClassList.add('question-radio-main-answer');
        questionCheckboxMainAnswer.classList.add('question-checkbox-main-answer');
        $(questionCheckboxMainAnswer).css({
            opacity: 1,
            display: 'inline',
        });
    } else {
        throw new ValidationError("createRadioOrCheckbox ERROR!!!");
    }
    questionMainAnswerRemove.prepend(questionMainAnswerRemoveImg);
    questionMainAnswersAnswer.append(questionRadioMainAnswer, questionCheckboxMainAnswer, questionMainAnswer, questionMainAnswerRemove);
    questionMainAnswers.append(questionMainAnswersAnswer);
}