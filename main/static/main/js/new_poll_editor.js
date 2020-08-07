$(function () {
    const maxAnswers = 15;
    const maxQuestions = 50;
    const maxLengthInput = 150;
    const timeAnimation = 200;

    const body = $('body');
    const pollHeader = $('.poll-editor__header');
    let listQuestions = {};

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
        if (val < 0) {
            val = 0;
        } else if (val > 100) {
            val = 100;
        } else if (typeof (val) !== typeof (10) || isNaN(val)) {
            val = 0;
        }
        $(this).val(val);
        if (val >= 0 && val <= 100) {
            let slider = $(this).closest('.slider-range').children('.mdc-slider');
            let _slider = new mdc.slider.MDCSlider(slider[0]);
            _slider.min = val;
        }
    });
    body.on('change', '.slider-range__max', function () {
        let val = parseInt($(this).val());
        if (val < 1) {
            val = 1;
        } else if (val > 100) {
            val = 100;
        } else if (typeof (val) !== typeof (10) || isNaN(val)) {
            val = 100;
        }
        $(this).val(val);
        if (val >= 1 && val <= 100) {
            let slider = $(this).closest('.slider-range').children('.mdc-slider');
            let _slider = new mdc.slider.MDCSlider(slider[0]);
            _slider.max = val;
        }
    });
    body.on('change', '.slider-range__step', function () {
        let val = parseInt($(this).val());
        let step = parseInt($(this).parent().parent().children('.max').children('.slider-range__max').val());
        if (val < 1) {
            val = 1;
        } else if (val > step) {
            val = step;
        } else if (typeof (val) !== typeof (10) || isNaN(val)) {
            val = 1;
        }
        $(this).val(val);
        if (val >= 1 && val <= 50) {
            let slider = $(this).closest('.slider-range').children('.mdc-slider');
            let _slider = new mdc.slider.MDCSlider(slider[0]);
            _slider.step = val;
        }
    });

    // Удаление вопросов
    body.on('click', '.question__urn', function () {
        let question = $(this).parent().parent();
        let questions = $(question).parent();
        if (questions.children('.question').length === 5) {
            console.log(questions.parent().children('.actions').children('.plus'))
            questions.parent().children('.actions').children('.plus').removeClass('hide')
        }
        let id = question.attr('data-question-id');
        // Удаляем из listQuestions
        delete listQuestions[id];
        question.remove();
        if (questions.children('.question').length === 0) {
            $('#nextToStep2').prop({
                'disabled': true,
            })
            // let newQuestion = createNewQuestion();
            // console.log(newQuestion)
            // questions.append(newQuestion);
        }
        console.log(listQuestions)
    });

    // Добавеление вопросов
    body.on('click', '.plus', function () {
        let questions = $('.questions');
        let newQuestion = createNewQuestion();
        console.log(newQuestion)
        questions.append(newQuestion);
        $('#nextToStep2').prop({
            'disabled': false,
        });
        // Заносим в listQuestions
        listQuestions[$(newQuestion).attr('data-question-id')] = {
            type: $(newQuestion).attr('data-question-type'),
        };
        console.log(listQuestions)

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
        location.href = '/polls/';
    });

    // Автоувеличение полей ввода
    function countLines(el, delta) {
        el.style.height = '1px';
        el.style.height = (el.scrollHeight + delta) + 'px';
    }

    // Первый запуск
    function run() {
        let questions = $('.question');
        if (questions.children('.question').length === 0) {
            $('#nextToStep2').prop({
                'disabled': true,
            });
        } else {
            $('#nextToStep2').prop({
                'disabled': false,
            });
        }

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
            // Заносим вопросы в список
            listQuestions[$(el).attr('data-question-id')] = {
                type: $(el).attr('data-question-type'),
            };
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
                console.log(lastVal, currentVal)

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
                console.log(answers)
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
                console.log(currentVal)
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
        let keys = Object.keys(listQuestions);
        for (let e in keys) {
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
});
