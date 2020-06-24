$(function () {
    const csrf = $('input[name="csrfmiddlewaretoken"]').val();
    let required = {
        'username': false,
        'pass1': false,
        'pass2': false,
        'email': false,
    };

    $('#id_username').on('input', function () {
        $.ajax({
            url: '',
            type: 'post',
            data: {
                id: $(this)[0].id,
                username: $(this)[0].value,
                csrfmiddlewaretoken: csrf,
            },
            success: function (response) {
                chooseValidationColor('#id_username', response.resultStatus);
                if (response.resultStatus === 'success') {
                    required.username = true;
                } else if (response.resultStatus === 'error') {
                    required.username = false;
                    showMessage(response.resultError);
                }
                checkBtnRegister(required);
            }
        });
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
                chooseValidationColor('#id_password1', response.result1Status);
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
                chooseValidationColor('#id_password2', response.resultStatus);
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
                chooseValidationColor('#id_email', response.resultStatus);
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

    $('#btn-register').click(function () {
        $.ajax({
            url: '',
            type: 'post',
            data: {
                id: $(this)[0].id,
                username: $('#id_username')[0].value,
                pass1: $('#id_password1')[0].value,
                pass2: $('#id_password2')[0].value,
                email: $('#id_email')[0].value,
                csrfmiddlewaretoken: csrf,
            },
        })
    });
});


function chooseValidationColor(id, status) {
    if (status === 'success') {
        if ($(id)[0].classList.contains('error')) {
            $(id)[0].classList.remove('error');
        }
        $(id)[0].classList.add('success');
    } else if (status === 'error') {
        if ($(id)[0].classList.contains('success')) {
            $(id)[0].classList.remove('success');
        }
        $(id)[0].classList.add('error');
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
