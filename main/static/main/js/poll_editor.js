$(function () {
    const poll_questions = $('.poll_questions');
    const body = $('body');

    // Настройка полей сразу после загрузки
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
    $('.question-main-answers-answer-range-settings-min, .question-main-answers-answer-range-settings-step, .question-main-answers-answer-range-settings-max').val(function () {
        $(this)[0].value = $(this)[0].value.replace(/[^\d]/g, '');
    });

    // Удаление опроса
    body.on('click', '.poll-head-remove', function (event) {
        event.preventDefault();
        if (confirm('Вы действительно хотите удалить данный опрос?')) {
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
    body.on('input', '.poll-head-name',  function () {
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
    body.on('input', '.question-main-answers-answer-range-settings-min, .question-main-answers-answer-range-settings-step, .question-main-answers-answer-range-settings-max',  function () {
        $(this)[0].value = $(this)[0].value.replace(/[^\d]/g, '');
    });

    // Смена типа вопроса
    body.on('input', '.question-settings-type_question', function () {
        let question = $(this).parent().parent();
        let questionMain = question.children('.question-main');
        let questionMainAnswers = questionMain.children('.question-main-answers');
        let lastType;
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
            console.log('question-settings-type_question ERROR!!!')
        }
        // Смена типа
        if ($(this)[0].value === 'radio') {
            question.addClass('question-radio');
            if (lastType === 'question-checkbox') {
                let answers = questionMainAnswers.children('.question-main-answers-answer');
                answers.children('.question-checkbox-main-answer').addClass('d-none');
                answers.children('.question-radio-main-answer').removeClass('d-none');
            } else {
                questionMainAnswers.children().remove();
                createRadioOrCheckbox('radio', questionMainAnswers, questionMain);
            }
        } else if ($(this)[0].value === 'checkbox') {
            question.addClass('question-checkbox');
            if (lastType === 'question-radio') {
                let answers = questionMainAnswers.children('.question-main-answers-answer');
                answers.children('.question-radio-main-answer').addClass('d-none');
                answers.children('.question-checkbox-main-answer').removeClass('d-none');
            } else {
                questionMainAnswers.children().remove();
                createRadioOrCheckbox('checkbox', questionMainAnswers, questionMain);
            }
        } else if ($(this)[0].value === 'range') {
            question.addClass('question-range');
            questionMainAnswers.children().remove();
            if (lastType === 'question-radio' || lastType === 'question-checkbox')
                questionMain.children('.question-main-add').remove();
            createRange(questionMainAnswers);
        } else if ($(this)[0].value === 'open_question') {
            question.addClass('question-open_question');
            questionMainAnswers.children().remove();
            if (lastType === 'question-radio' || lastType === 'question-checkbox')
                questionMain.children('.question-main-add').remove();
            createOpenQuestion(questionMainAnswers);
        } else {
            console.log('question-settings-type_question ERROR!!!')
        }
    });

    // Добавление варианта ответа
    body.on('click', '.question-main-add', function () {
        let questions = $(this).
    });

    // Добавление вопроса
    body.on('click', '.poll_questions-navigate-add_question', function () {
        createNewQuestion(poll_questions);
    });

    // Перемещение вопросов
    poll_questions.sortable();
});

// Автоувеличение полей ввода
function countLines(el, delta) {
    el.style.height = '1px';
    el.style.height = (el.scrollHeight + delta) + 'px';
}

function createRadioOrCheckbox(type, questionMainAnswers, questionMain) {
    let questionMainAnswersAnswer = document.createElement('div');
    questionMainAnswersAnswer.classList.add('question-main-answers-answer');
    let questionRadioMainAnswerNumber = document.createElement('span');
    let questionCheckboxMainAnswer = document.createElement('span');
    let questionMainAnswer = document.createElement('textarea');
    questionMainAnswer.classList.add('question-main-answer');
    questionMainAnswer.name = '';
    questionMainAnswer.id = '';
    questionMainAnswer.rows = 1;
    questionMainAnswer.placeholder = 'Вариант 1';
    questionMainAnswer.setAttribute('data-number_answer', '1');
    let questionMainAnswerRemove = document.createElement('button');
    questionMainAnswerRemove.classList.add('question-main-answer-remove');
    let questionMainAnswerRemoveImg = document.createElement('img');
    questionMainAnswerRemoveImg.classList.add('question-main-answer-remove-img');
    questionMainAnswerRemoveImg.src = '../../static/main/images/cross.svg';
    questionMainAnswerRemoveImg.alt = '';
    if (type === 'radio') {
        questionRadioMainAnswerNumber.classList.add('question-radio-main-answer');
        let questionCheckboxMainAnswerClassList = questionCheckboxMainAnswer.classList;
        questionCheckboxMainAnswerClassList.add('question-checkbox-main-answer');
        questionCheckboxMainAnswerClassList.add('d-none');
    } else if (type === 'checkbox') {
        let questionRadioMainAnswerNumberClassList = questionRadioMainAnswerNumber.classList;
        questionRadioMainAnswerNumberClassList.add('question-radio-main-answer');
        questionRadioMainAnswerNumberClassList.add('d-none');
        questionCheckboxMainAnswer.classList.add('question-checkbox-main-answer');
    } else {
        console.log('createRadioOrCheckbox ERROR!!!');
        return;
    }
    questionMainAnswerRemove.prepend(questionMainAnswerRemoveImg);
    questionMainAnswersAnswer.append(questionRadioMainAnswerNumber, questionCheckboxMainAnswer, questionMainAnswer, questionMainAnswerRemove);
    questionMainAnswers.append(questionMainAnswersAnswer);
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
    // questionSettingsType_questionOption2.selected=false;
    questionSettingsType_questionOption2.text = 'Несколько из списка';
    let questionSettingsType_questionOption3 = document.createElement('option');
    questionSettingsType_questionOption3.value = 'range';
    questionSettingsType_questionOption3.classList.add('question-settings-type_question-option');
    // questionSettingsType_questionOption3.selected=false;
    questionSettingsType_questionOption3.text = 'Шкала';
    let questionSettingsType_questionOption4 = document.createElement('option');
    questionSettingsType_questionOption4.value = 'open_question';
    questionSettingsType_questionOption4.classList.add('question-settings-type_question-option');
    // questionSettingsType_questionOption4.selected=false;
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

    question.append(questionMain, questionSettings, questionNavigate);
    poll_questions.append(question);
}