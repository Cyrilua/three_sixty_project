$(function () {
    const body = $('body');
    const csrf = $('input[name="csrfmiddlewaretoken"]').val();
    const timeShow = 300;

    let required = {
        'username': false,
        'password1': false,
        'password2': false,
        'email': false,
        'fullname': false,
        'birthday': false,
    };

    let errors = {
        'username': false,
        'password1': false,
        'password2': false,
        'email': false,
        'birthday': false,
    };

    $(body).on('click', '.register-form-navigate-btn-next_step', function (event) {
        event.preventDefault();
        $('.step-1').addClass('d-none');
        $('.step-2').removeClass('d-none');
    });

    body.on('click', '.register-form-navigate-btn-back_step', function (event) {
        event.preventDefault();
        $('.step-2').addClass('d-none');
        $('.step-1').removeClass('d-none');
    });

    //################################################

    body.on('focus', '.input-field', function () {
        console.log('show')
        for (let key in errors) {
            let name = $(this)[0].name;
            if (key === name) {
                if (errors[key]) {
                    $(this).parent().children('.popup').css({
                        display: 'block',
                        opacity: 0,
                    })
                        .stop().animate({
                        opacity: 1,
                    }, timeShow);
                } else {
                    break;
                }
            }
        }
    });

    body.on('focusout', '.input-field', function () {
        console.log('no show')
        $(this).parent().children('.popup').stop().animate({
            opacity: 0,
        }, timeShow, function () {
            $(this).css({
                display: 'none',
            });
        });
    });

    $('#id_username').on('input', function () {
        let el = $(this)[0];
        el.value = el.value.toLowerCase();
        let checker = checkFieldValidation(RegExp('[a-z][a-z0-9]+'), 3, 20, el.value);
        chooseValidationColor(el, checker);
        if (checker === 'success') {
            $.ajax({
                url: '',
                type: 'post',
                data: {
                    id: $(this)[0].id,
                    username: $(this)[0].value,
                    csrfmiddlewaretoken: csrf,
                },
                success: function (response) {
                    chooseValidationColor($('#id_username')[0], response.resultStatus);
                    if (response.resultStatus === 'success') {
                        required.username = true;
                        errors.username = false;
                        removeErrors(body, el, response.resultError, timeShow);
                    } else if (response.resultStatus === 'error') {
                        required.username = false;
                        errors.username = true;
                        showErrors(body, el, response.resultError, timeShow);
                    }
                    checkBtnRegister(required);
                }
            });
        }
    });

    $('#id_password1').on('input', function () {
        $.ajax({
            url: '',
            type: 'post',
            data: {
                id: $(this)[0].id,
                password1: $(this)[0].value,
                csrfmiddlewaretoken: csrf,
            },
            success: function (response) {
                chooseValidationColor($('#id_password1')[0], response.resultStatus);
                if (response.resultStatus === 'success') {
                    required.password1 = true;
                    $('#id_password2').prop({
                        'disabled': false,
                    });
                } else if (response.resultStatus === 'error') {
                    required.password1 = false;
                    showErrors(response.resultError);
                    $('#id_password2').prop({
                        'disabled': true,
                    });
                }
                checkBtnRegister(required);
            }
        });
    });

    $('#id_password2').on('input', function () {
        $.ajax({
            url: '',
            type: 'post',
            data: {
                id: $(this)[0].id,
                password1: $('#id_password1')[0].value,
                password2: $(this)[0].value,
                csrfmiddlewaretoken: csrf,
            },
            success: function (response) {
                chooseValidationColor($('#id_password2')[0], response.resultStatus);
                if (response.resultStatus === 'success') {
                    required.password2 = true;
                } else if (response.resultStatus === 'error') {
                    required.password2 = false;
                    showErrors(response.resultError);
                }
                checkBtnRegister(required);
            }
        });
    });

    $('#id_email').on('input', function () {
        $.ajax({
            url: '',
            type: 'post',
            data: {
                id: $(this)[0].id,
                email: $(this)[0].value,
                csrfmiddlewaretoken: csrf,
            },
            success: function (response) {
                chooseValidationColor($('#id_email')[0], response.resultStatus);
                if (response.resultStatus === 'success') {
                    required.email = true;
                } else if (response.resultStatus === 'error') {
                    required.email = false;
                    showErrors(response.resultError);
                }
                checkBtnRegister(required);
            }
        });
    });

    $('#id_fullname').on('input', function () {
        let el = $(this)[0];
        formatValue(el);
        let checker = checkFieldValidation(RegExp(''), 6, 150, el.value);
        console.log(checker);
        chooseValidationColor(el, checker);
        if (checker === 'success') {
            required.fullname = true;
        } else if (checker === 'error') {
            required.fullname = false;
            showErrors("ERROR");
        }
        checkBtnRegister(required);
    });

    $('#id_birthday').on('input', function () {
        let el = $(this);
        let checker = checkBirthday($(this)[0], 1900, 15);
        if (el.value !== '' && checker) {
            $(this).removeClass('error');
            required.birthday = true;
        } else {
            $(this).addClass('error');
            required.birthday = false;
            showErrors('Error!');
        }
        checkBtnRegister(required);
    });
});


// Первая буква заглавная, остальные строчные
function formatValue(element) {
    if (element.value !== '' && element.value[0] !== element.value[0].toUpperCase()) {
        let position = element.selectionStart;
        element.value = element.value[0].toUpperCase() + element.value.slice(1).toLowerCase();
        element.selectionStart = element.selectionEnd = position;
    }
}

// Проверка полей на правильность ввода
function checkFieldValidation(regexp, minLen, maxLen, str) {
    if (regexp.test(str) && str.length >= minLen && str.length <= maxLen) {
        return 'success';
    }
    return 'error';
}

// Выбор цвета поля (отображение валидности полей)
function chooseValidationColor(element, status) {
    if (status === 'success') {
        if (element.classList.contains('error')) {
            element.classList.remove('error');
        }
        // element.classList.add('success');
    } else if (status === 'error') {
        // if (element.classList.contains('success')) {
        //     element.classList.remove('success');
        // }
        element.classList.add('error');
    }
}

function showErrors(body, el, errors, timeShow) {
    let popup = $(el).parent().children('.popup');
    let alert = popup.children('.popup_message');
    alert.children().remove();
    for (let i = 0; i < errors.length; i++) {
        let span = document.createElement('span');
        span.classList.add('popup_message-text');
        span.textContent = errors[i];
        alert.append(span);
    }
    popup
        .css({
            display: 'block',
            opacity: 0,
        })
        .stop().animate({
        opacity: 1,
    }, timeShow);
}

function removeErrors(body, el, errors, timeShow) {
    let popup = $(el).parent().children('.popup');
    let alert = popup.children('.popup_message');
    popup.stop().animate({
        opacity: 0,
    }, timeShow, function () {
        $(this).css({
            display: 'none',
        });
        alert.children().remove();
    });

}

// Проверка, что все поля заполнены и кнопку "Зарегистрироваться" можно нажать
function checkBtnRegister(required) {
    if (isTrueAllinObj(required)) {
        $('#btn-register').prop({
            'disabled': false,
        })
    } else {
        $('#btn-register').prop({
            'disabled': true,
        })
    }
}

//Проверка объекта (required), что все свойства true
function isTrueAllinObj(obj) {
    for (let key in obj) {
        if (obj[key] === false) {
            return false;
        }
    }
    return true;
}

function checkBirthday(el, min, deltaMax) {
    let year = el.value.split('-')[0];
    let currentYear = (new Date()).getFullYear();
    return year >= min && year <= currentYear - deltaMax;
}