$(function () {
    const csrf = $('input[name="csrfmiddlewaretoken"]').val();
    let required = {
        'username': false,
        'pass1': false,
        'pass2': false,
        'email': false,
        'name': false,
        'surname': false,
        'patronymic': false,
        'city': false,
    };

    $('#id_username').on('input', function () {
        let el = $(this)[0];
        el.value = el.value.toLowerCase();
        let checker = checkFieldValidation(RegExp('[a-z][a-z0-9]+'), 5, 20, el.value);
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
                    } else if (response.resultStatus === 'error') {
                        required.username = false;
                        showMessage(response.resultError);
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
                pass1: $(this)[0].value,
                csrfmiddlewaretoken: csrf,
            },
            success: function (response) {
                chooseValidationColor($('#id_password1')[0], response.resultStatus);
                if (response.resultStatus === 'success') {
                    required.pass1 = true;
                    $('#id_password2').prop({
                        'disabled': false,
                    });
                } else if (response.resultStatus === 'error') {
                    required.pass1 = false;
                    showMessage(response.resultError);
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
                pass1: $('#id_password1')[0].value,
                pass2: $(this)[0].value,
                csrfmiddlewaretoken: csrf,
            },
            success: function (response) {
                chooseValidationColor($('#id_password2')[0], response.resultStatus);
                if (response.resultStatus === 'success') {
                    required.pass2 = true;
                } else if (response.resultStatus === 'error') {
                    required.pass2 = false;
                    showMessage(response.resultError);
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
                    showMessage(response.resultError);
                }
                checkBtnRegister(required);
            }
        });
    });

    $('#id_name').on('input', function () {
        let el = $(this)[0];
        formatValue(el);
        let checker = checkFieldValidation(RegExp('[А-Яа-я][а-я]+'), 2, 20, el.value);
        console.log(checker);
        chooseValidationColor(el, checker);
        if (checker === 'success') {
            required.name = true;
        } else if (checker === 'error') {
            required.name = false;
            showMessage("ERROR");
        }
        checkBtnRegister(required);
    });

    $('#id_surname').on('input', function () {
        let el = $(this)[0];
        formatValue(el);
        let checker = checkFieldValidation(RegExp('[А-Яа-я][а-я]+'), 2, 20,  el.value);
        console.log(checker);
        chooseValidationColor(el, checker);
        if (checker === 'success') {
            required.surname = true;
        } else if (checker === 'error') {
            required.surname = false;
            showMessage("ERROR");
        }
        checkBtnRegister(required);
    });

    $('#id_patronymic').on('input', function () {
        let el = $(this)[0];
        formatValue(el);
        let checker = checkFieldValidation(RegExp('[А-Яа-я][а-я]+'), 5, 20,  el.value);
        console.log(checker);
        chooseValidationColor(el, checker);
        if (checker === 'success') {
            required.patronymic = true;
        } else if (checker === 'error') {
            required.patronymic = false;
            showMessage("ERROR");
        }
        checkBtnRegister(required);
    });

    $('#id_city').on('change', function () {
        console.log($(this)[0].value);
        chooseValidationColor($(this)[0], 'success');
        required.city = true;
        checkBtnRegister(required);
    });

    // $('#btn-register').click(function () {
    //     $.ajax({
    //         url: '',
    //         type: 'post',
    //         data: {
    //             id: $('#btn-register')[0].id,
    //             username: $('#id_username')[0].value,
    //             pass1: $('#id_password1')[0].value,
    //             pass2: $('#id_password2')[0].value,
    //             email: $('#id_email')[0].value,
    //             name: $('#id_name')[0].value,
    //             surname: $('#id_surname')[0].value,
    //             patronymic: $('#id_patronymic')[0].value,
    //             city: $('#id_city')[0].value,
    //             csrfmiddlewaretoken: csrf,
    //         },
    //     });
    // });
});


function formatValue(element) {
    if (element.value !== '' && element.value[0] !== element.value[0].toUpperCase()) {
        let position = element.selectionStart;
        element.value = element.value[0].toUpperCase() + element.value.slice(1).toLowerCase();
        element.selectionStart = element.selectionEnd = position;
    }
}

function checkFieldValidation(regexp, minLen, maxLen, str) {
    if (regexp.test(str) && str.length >= minLen && str.length <= maxLen) {
        return 'success';
    }
    return 'error';
}

function chooseValidationColor(element, status) {
    if (status === 'success') {
        if (element.classList.contains('error')) {
            element.classList.remove('error');
        }
        element.classList.add('success');
    } else if (status === 'error') {
        if (element.classList.contains('success')) {
            element.classList.remove('success');
        }
        element.classList.add('error');
    }
}

function showMessage(message) {
    //TODO Вывод ошибок при валидации
}

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
