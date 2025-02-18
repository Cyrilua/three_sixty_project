$(function () {
    const body = $('body');
    const csrf = $('input[name="csrfmiddlewaretoken"]').val();
    const timeShow = 300;

    let username = $('#id_username');
    let password1 = $('#id_password1');
    let password2 = $('#id_password2');
    let email = $('#id_email');
    let name = $('#id_name');
    let surname = $('#id_surname');
    let patronymic = $('#id_patronymic');
    let birthday = $('#id_birthday');
    let code = $('#code');

    let required = {
        'username': false,
        'password1': false,
        'password2': false,
        'email': false,
        'name': false,
        'surname': false,
        'patronymic': false,
        'birthday': false,
        'code': false,
    };

    let errors = {
        'username': false,
        'password1': false,
        'password2': false,
        'email': false,
        'name': false,
        'surname': false,
        'patronymic': false,
        'birthday': false,
        'code': false,
    };

    username.val('');
    password1.val('');
    password2.val('');
    password2.prop({
        'disabled': true,
    });
    email.val('');
    name.val('');
    surname.val('');
    patronymic.val('');
    birthday.val('');
    checkBtnNext(required);
    checkBtnRegister(required);
    code.val('');

    // if (username.val() !== '')
    //     ajaxForUsername(username, csrf, required, errors, body, timeShow);
    // if (password1.val() !== '')
    //     ajaxForPassword1(password1, csrf, required, errors, body, timeShow);
    // if (password2.val() !== '')
    //     ajaxForPassword2(password2, csrf, required, errors, body, timeShow);
    // if (email.val() === '')
    //     ajaxForEmail(email, csrf, required, errors, body, timeShow);
    // if (fullname.val() === '')
    //     ajaxForName(fullname, csrf, required, errors, body, timeShow);
    // if (birthday.val() === '')
    //     ajaxForBirthday(birthday, csrf, required, errors, body, timeShow);


    // Кастомный календарь
    if (birthday.prop('type') !== 'date') {
        birthday.datepicker({
            onSelect: function (formattedDate, date, inst) {
                let el = birthday;
                $.ajax({
                    url: '',
                    type: 'post',
                    data: {
                        id: birthday[0].id,
                        birthday: formattedDate,
                        csrfmiddlewaretoken: csrf,
                    },
                    success: function (response) {
                        chooseValidationColor($('#id_birthday')[0], response.resultStatus);
                        if (response.resultStatus === 'success') {
                            required.birthday = true;
                            errors.birthday = false;
                            removeErrors(el, timeShow);
                        } else if (response.resultStatus === 'error') {
                            required.birthday = false;
                            errors.birthday = true;
                            showErrors(body, el, response.resultError, timeShow);
                        }
                        checkBtnRegister(required);
                        checkBtnNext(required);
                    },
                    statusCode: {
                        400: function () {
                            throw new Error('Error 400 - Некорректный запрос');
                        },
                        403: function () {
                            throw new Error('Error 403 - Доступ запрещён');
                        },
                        404: function () {
                            throw new Error('Error 404 - Страница не найдена');
                        },
                        500: function () {
                            throw new Error('Error 500 - Внутренняя ошибка сервера');
                        }
                    },
                    error: function () {
                        throw new Error('Что - то пошло не так :(');
                    }
                });
            },
            dateFormat: 'd.m.yyyy',
            position: 'top left',
        });
    }

    // next-2
    body.on('click', '#next-2', function (event) {
        event.preventDefault();
        $('.step-1').addClass('hide');
        $('.step-2').removeClass('hide');
    });

    // back-1
    body.on('click', '#back-1', function (event) {
        event.preventDefault();
        $('.step-2').addClass('hide');
        $('.step-1').removeClass('hide');
    });

    // next-3
    body.on('click', '#next-3', function (event) {
        event.preventDefault();
        let partUrl = $(this).attr('data-part-url');
        $.ajax({
            url: `register/${partUrl}`,
            type: 'post',
            data: {
                surname: surname.val(),
                name: name.val(),
                email: email.val(),
                csrfmiddlewaretoken: csrf,
                host: location.hostname,
            },
            beforeSend: function () {
                $('.step-2').addClass('hide');
                $('.step-3').removeClass('hide');
            },
            statusCode: {
                400: function () {
                    throw new Error('Error 400 - Некорректный запрос');
                },
                403: function () {
                    throw new Error('Error 403 - Доступ запрещён');
                },
                404: function () {
                    throw new Error('Error 404 - Страница не найдена');
                },
                500: function () {
                    throw new Error('Error 500 - Внутренняя ошибка сервера');
                }
            },
            error: function () {
                throw new Error('Что - то пошло не так :(');
            }
        })
    });

    // back-2
    body.on('click', '#back-2', function (event) {
        event.preventDefault();
        $('.step-3').addClass('hide');
        $('.step-2').removeClass('hide');
    });

    // Вывод шибки при фокусе на поле
    body.on('focus', '.input-field', function () {
        for (let key in errors) {
            let name = $(this)[0].name;
            if (key === name) {
                if (errors[key]) {
                    let popup = $(this).parent().children('.popup');
                    popup.css({
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

    // Скрытие ошибки при расфокусировке поля
    body.on('focusout', '.input-field', function () {
        $(this).parent().children('.popup').stop().animate({
            opacity: 0,
        }, timeShow, function () {
            $(this).css({
                display: 'none',
            });
        });
    });

    // Обработка полей
    body.on('input', '#id_username', function () {
        let el = $(this);
        ajaxForUsername(el, csrf, required, errors, body, timeShow);
    });

    body.on('input', '#id_password1', function () {
        let el = $(this);
        ajaxForPassword1(el, csrf, required, errors, body, timeShow);
    });

    body.on('input', '#id_password2', function () {
        let el = $(this);
        ajaxForPassword2(el, csrf, required, errors, body, timeShow);
    });

    body.on('input', '#id_email', function () {
        let el = $(this);
        ajaxForEmail(el, csrf, required, errors, body, timeShow);
    });

    body.on('input', '#id_name', function () {
        let el = $(this);
        ajaxForName(el, csrf, required, errors, body, timeShow);
    });

    body.on('input', '#id_surname', function () {
        let el = $(this);
        ajaxForSurname(el, csrf, required, errors, body, timeShow);
    });

    body.on('input', '#id_patronymic', function () {
        let el = $(this);
        ajaxForPatronymic(el, csrf, required, errors, body, timeShow);
    });

    body.on('input', '#id_birthday', function () {
        let el = $(this);
        ajaxForBirthday(el, csrf, required, errors, body, timeShow);
    });

    body.on('input', '#code', function () {
        let el = $(this);
        required.code = el.val().length > 0;
        checkBtnDone(required);
    });

    body.on('mouseup', '#btn-register', function (el) {
        let partUrl = $(this).attr('data-part-url');
        $.ajax({
            url: `register/${partUrl}`,
            type: 'post',
            data: {
                code: code.val(),
                email: email.val(),
                csrfmiddlewaretoken: csrf,
            },
            success: function (response) {
                chooseValidationColor(el.target, response.resultStatus);
                if (response.resultStatus === 'success') {
                    el.target.type = 'submit';
                    $(el.target).trigger('click');
                } else if (response.resultStatus === 'error') {
                    required.code = false;
                    errors.code = true;
                    chooseValidationColor(code[0], response.resultStatus);
                    showErrors(body, code, response.listErrors, timeShow);
                    code.focus();
                    checkBtnDone(required);
                }
            },
            statusCode: {
                400: function () {
                    throw new Error('Error 400 - Некорректный запрос');
                },
                403: function () {
                    throw new Error('Error 403 - Доступ запрещён');
                },
                404: function () {
                    throw new Error('Error 404 - Страница не найдена');
                },
                500: function () {
                    throw new Error('Error 500 - Внутренняя ошибка сервера');
                }
            },
            error: function () {
                throw new Error('Что - то пошло не так :(');
            }
        });
    });
});


// Первая буква заглавная, остальные строчные
function formatValue(el) {
    let element = el[0];
    if (element.value !== '') {
        let position = element.selectionStart;
        element.value = element.value[0].toUpperCase() + element.value.slice(1).toLowerCase();
        element.selectionStart = element.selectionEnd = position;
    }
}

// // Проверка полей на правильность ввода
// function checkFieldValidation(regexp, minLen, maxLen, str) {
//     if (regexp.test(str) && str.length >= minLen && str.length <= maxLen) {
//         return 'success';
//     }
//     return 'error';
// }

function ajaxForUsername(el, csrf, required, errors, body, timeShow) {
    el[0].value = el[0].value.toLowerCase();
    $.ajax({
        url: '',
        type: 'post',
        data: {
            id: el[0].id,
            username: el[0].value,
            csrfmiddlewaretoken: csrf,
        },
        success: function (response) {
            chooseValidationColor(el[0], response.resultStatus);
            if (response.resultStatus === 'success') {
                required.username = true;
                errors.username = false;
                removeErrors(el, timeShow);
            } else if (response.resultStatus === 'error') {
                required.username = false;
                errors.username = true;
                showErrors(body, el, response.resultError, timeShow);
            }
            checkBtnRegister(required);
            checkBtnNext(required);
        },
        statusCode: {
            400: function () {
                throw new Error('Error 400 - Некорректный запрос');
            },
            403: function () {
                throw new Error('Error 403 - Доступ запрещён');
            },
            404: function () {
                throw new Error('Error 404 - Страница не найдена');
            },
            500: function () {
                throw new Error('Error 500 - Внутренняя ошибка сервера');
            }
        },
        error: function () {
            throw new Error('Что - то пошло не так :(');
        }
    });
}

function ajaxForPassword1(el, csrf, required, errors, body, timeShow,) {
    let pass2 = $('#id_password2');
    $.ajax({
        url: '',
        type: 'post',
        data: {
            id: el[0].id,
            password1: el[0].value,
            password2: pass2[0].value,
            csrfmiddlewaretoken: csrf,
        },
        success: function (response) {
            chooseValidationColor(el[0], response.resultStatus);
            if (response.resultStatus === 'success') {
                required.password1 = true;
                errors.password1 = false;
                removeErrors(el, timeShow);
                let pass2 = $('#id_password2');
                pass2.prop({
                    'disabled': false,
                });
                pass2.val('');
                required.password2 = false;
                errors.password2 = false;
            } else if (response.resultStatus === 'error') {
                required.password1 = false;
                errors.password1 = true;
                showErrors(body, el, response.resultError, timeShow);
                $('#id_password2').prop({
                    'disabled': true,
                });
            }
            checkBtnRegister(required);
            checkBtnNext(required);
        },
        statusCode: {
            400: function () {
                throw new Error('Error 400 - Некорректный запрос');
            },
            403: function () {
                throw new Error('Error 403 - Доступ запрещён');
            },
            404: function () {
                throw new Error('Error 404 - Страница не найдена');
            },
            500: function () {
                throw new Error('Error 500 - Внутренняя ошибка сервера');
            }
        },
        error: function () {
            throw new Error('Что - то пошло не так :(');
        }
    });
}

function ajaxForPassword2(el, csrf, required, errors, body, timeShow) {
    let pass1 = $('#id_password1');
    $.ajax({
        url: '',
        type: 'post',
        data: {
            id: el[0].id,
            password1: pass1[0].value,
            password2: el[0].value,
            csrfmiddlewaretoken: csrf,
        },
        success: function (response) {
            chooseValidationColor(el[0], response.resultStatus);
            if (response.resultStatus === 'success') {
                required.password2 = true;
                errors.password2 = false;
                removeErrors(el, timeShow);
            } else if (response.resultStatus === 'error') {
                required.password2 = false;
                errors.password2 = true;
                showErrors(body, el, response.resultError, timeShow);
            }
            checkBtnRegister(required);
            checkBtnNext(required);
        },
        statusCode: {
            400: function () {
                throw new Error('Error 400 - Некорректный запрос');
            },
            403: function () {
                throw new Error('Error 403 - Доступ запрещён');
            },
            404: function () {
                throw new Error('Error 404 - Страница не найдена');
            },
            500: function () {
                throw new Error('Error 500 - Внутренняя ошибка сервера');
            }
        },
        error: function () {
            throw new Error('Что - то пошло не так :(');
        }
    });
}

function ajaxForEmail(el, csrf, required, errors, body, timeShow) {
    $.ajax({
        url: '',
        type: 'post',
        data: {
            id: el[0].id,
            email: el[0].value,
            csrfmiddlewaretoken: csrf,
        },
        success: function (response) {
            chooseValidationColor(el[0], response.resultStatus);
            if (response.resultStatus === 'success') {
                required.email = true;
                errors.email = false;
                removeErrors(el, timeShow);
            } else if (response.resultStatus === 'error') {
                required.email = false;
                errors.email = true;
                showErrors(body, el, response.resultError, timeShow);
            }
            checkBtnRegister(required);
            checkBtnNext(required);
        },
        statusCode: {
            400: function () {
                throw new Error('Error 400 - Некорректный запрос');
            },
            403: function () {
                throw new Error('Error 403 - Доступ запрещён');
            },
            404: function () {
                throw new Error('Error 404 - Страница не найдена');
            },
            500: function () {
                throw new Error('Error 500 - Внутренняя ошибка сервера');
            }
        },
        error: function () {
            throw new Error('Что - то пошло не так :(');
        }
    });
}

function ajaxForName(el, csrf, required, errors, body, timeShow) {
    formatValue(el);
    $.ajax({
        url: '',
        type: 'post',
        data: {
            id: el[0].id,
            name: el[0].value,
            csrfmiddlewaretoken: csrf,
        },
        success: function (response) {
            chooseValidationColor(el[0], response.resultStatus);
            if (response.resultStatus === 'success') {
                required.name = true;
                errors.name = false;
                removeErrors(el, timeShow);
            } else if (response.resultStatus === 'error') {
                required.name = false;
                errors.name = true;
                showErrors(body, el, response.resultError, timeShow);
            }
            checkBtnRegister(required);
            // checkBtnNext(required);
        },
        statusCode: {
            400: function () {
                throw new Error('Error 400 - Некорректный запрос');
            },
            403: function () {
                throw new Error('Error 403 - Доступ запрещён');
            },
            404: function () {
                throw new Error('Error 404 - Страница не найдена');
            },
            500: function () {
                throw new Error('Error 500 - Внутренняя ошибка сервера');
            }
        },
        error: function () {
            throw new Error('Что - то пошло не так :(');
        }
    });
}

function ajaxForSurname(el, csrf, required, errors, body, timeShow) {
    formatValue(el);
    $.ajax({
        url: '',
        type: 'post',
        data: {
            id: el[0].id,
            surname: el[0].value,
            csrfmiddlewaretoken: csrf,
        },
        success: function (response) {
            chooseValidationColor(el[0], response.resultStatus);
            if (response.resultStatus === 'success') {
                required.surname = true;
                errors.surname = false;
                removeErrors(el, timeShow);
            } else if (response.resultStatus === 'error') {
                required.surname = false;
                errors.surname = true;
                showErrors(body, el, response.resultError, timeShow);
            }
            checkBtnRegister(required);
            // checkBtnNext(required);
        },
        statusCode: {
            400: function () {
                throw new Error('Error 400 - Некорректный запрос');
            },
            403: function () {
                throw new Error('Error 403 - Доступ запрещён');
            },
            404: function () {
                throw new Error('Error 404 - Страница не найдена');
            },
            500: function () {
                throw new Error('Error 500 - Внутренняя ошибка сервера');
            }
        },
        error: function () {
            throw new Error('Что - то пошло не так :(');
        }
    });
}

function ajaxForPatronymic(el, csrf, required, errors, body, timeShow) {
    formatValue(el);
    $.ajax({
        url: '',
        type: 'post',
        data: {
            id: el[0].id,
            patronymic: el[0].value,
            csrfmiddlewaretoken: csrf,
        },
        success: function (response) {
            chooseValidationColor(el[0], response.resultStatus);
            if (response.resultStatus === 'success') {
                required.patronymic = true;
                errors.patronymic = false;
                removeErrors(el, timeShow);
            } else if (response.resultStatus === 'error') {
                required.patronymic = false;
                errors.patronymic = true;
                showErrors(body, el, response.resultError, timeShow);
            }
            checkBtnRegister(required);
            // checkBtnNext(required);
        },
        statusCode: {
            400: function () {
                throw new Error('Error 400 - Некорректный запрос');
            },
            403: function () {
                throw new Error('Error 403 - Доступ запрещён');
            },
            404: function () {
                throw new Error('Error 404 - Страница не найдена');
            },
            500: function () {
                throw new Error('Error 500 - Внутренняя ошибка сервера');
            }
        },
        error: function () {
            throw new Error('Что - то пошло не так :(');
        }
    });
}

function ajaxForBirthday(el, csrf, required, errors, body, timeShow) {
    $.ajax({
        url: '',
        type: 'post',
        data: {
            id: el[0].id,
            birthday: el[0].value,
            csrfmiddlewaretoken: csrf,
        },
        success: function (response) {
            chooseValidationColor(el[0], response.resultStatus);
            if (response.resultStatus === 'success') {
                required.birthday = true;
                errors.birthday = false;
                removeErrors(el, timeShow);
            } else if (response.resultStatus === 'error') {
                required.birthday = false;
                errors.birthday = true;
                showErrors(body, el, response.resultError, timeShow);
            }
            checkBtnRegister(required);
            // checkBtnNext(required);
        },
        statusCode: {
            400: function () {
                throw new Error('Error 400 - Некорректный запрос');
            },
            403: function () {
                throw new Error('Error 403 - Доступ запрещён');
            },
            404: function () {
                throw new Error('Error 404 - Страница не найдена');
            },
            500: function () {
                throw new Error('Error 500 - Внутренняя ошибка сервера');
            }
        },
        error: function () {
            throw new Error('Что - то пошло не так :(');
        }
    });
}

// Выбор цвета поля (отображение валидности полей)
function chooseValidationColor(element, status) {
    if (status === 'success') {
        if (element.classList.contains('error')) {
            element.classList.remove('error');
        }
    } else if (status === 'error') {
        element.classList.add('error');
    }
}

// Появление ошибок
function showErrors(body, el, errors, timeShow) {
    // console.log(errors)
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

// Удаление ошибок
function removeErrors(el, timeShow) {
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

// Проверка, что все поля заполнены и кнопку "Далее" (2 страница) можно нажать
function checkBtnRegister(required) {
    if (isTrueAllinObj(required, false)) {
        $('#next-3').prop({
            disabled: false,
        })
    } else {
        $('#next-3').prop({
            disabled: true,
        })
    }
}

// Проверка, что все поля страницы 1 заполнены и кнопку "Далее" (1 страница) можно нажать
function checkBtnNext(required) {
    if (required.username === true && required.email === true && required.password1 === true && required.password2 === true) {
        $('#next-2').prop({
            disabled: false
        })
    } else {
        $('#next-2').prop({
            disabled: true
        })
    }
}

// Проверка, что все поля заполнены и кнопку "Готово" можно нажать
function checkBtnDone(required) {
    if (isTrueAllinObj(required, true)) {
        $('#btn-register').prop({
            disabled: false,
        })
    } else {
        $('#btn-register').prop({
            disabled: true,
        })
    }
}

//Проверка объекта (required), что все свойства true
function isTrueAllinObj(obj, code) {
    for (let key in obj) {
        if (key !== 'code') {
            if (obj[key] === false) {
                return false;
            }
        } else if (code) {
            if (obj[key] === false) {
                return false;
            }
        }
    }
    return true;
}

// function checkBirthday(el, min, deltaMax) {
//     let year = el.value.split('-')[0];
//     let currentYear = (new Date()).getFullYear();
//     return year >= min && year <= currentYear - deltaMax;
// }