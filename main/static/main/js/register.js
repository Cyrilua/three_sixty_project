$(function () {
    const csrf = $('input[name="csrfmiddlewaretoken"]').val();
    let username = '';
    let email = '';
    let required = {
        'username': false,
        'pass1': false,
        'pass2': false,
        'email': false,
    };

    $('#id_username').focusout(function () {
        if ($(this).val() !== username) {
            $.ajax({
                url: '',
                type: 'post',
                data: {
                    id: $(this).id,
                    username: $(this).val(),
                    csrfmiddlewaretoken: csrf,
                },
                success: function (response) {
                    chooseValidationColor('#id_username', response.usernameStatus);
                    if (response.usernameStatus === 'success') {
                        required.username = true;
                    } else if (response.usernameStatus === 'error') {
                        required.username = false;
                        showMessage(response.usernameError);
                    }
                }
            });
            checkBtnRegister(required);
            username = $(this).val();
        }
    });

    $('#id_password1').focusout(function () {
        $.ajax({
            url: '',
            type: 'post',
            data: {
                id: $(this).id,
                pass1: $(this).val(),
                csrfmiddlewaretoken: csrf,
            },
            success: function (response) {
                chooseValidationColor('#id_username', response.password1Status);
                if (response.password1Status === 'success') {
                    required.pass1 = true;
                    $('#id_password2').prop({
                        'disabled': false,
                    });
                } else if (response.password1Status === 'error') {
                    required.pass1 = false;
                    showMessage(response.password1Error);
                    $('#id_password2').prop({
                        'disabled': true,
                    });
                }
            }
        });
        checkBtnRegister(required);
    });

    $('#id_password2').focusout(function () {
        $.ajax({
            url: '',
            type: 'post',
            data: {
                id: $(this).id,
                pass1: $('#id_password1').val(),
                pass2: $(this).val(),
                csrfmiddlewaretoken: csrf,
            },
            success: function (response) {
                chooseValidationColor('#id_username', response.password2Status);
                if (response.password2Status === 'success') {
                    required.pass2 = true;
                } else if (response.password2Status === 'error') {
                    required.pass2 = false;
                    showMessage(response.password2Error);
                }
            }
        });
        checkBtnRegister(required);
    });

    $('#id_email').focusout(function () {
        if ($(this).val() !== email) {
            $.ajax({
                url: '',
                type: 'post',
                data: {
                    id: $(this).id,
                    email: $(this).val(),
                    csrfmiddlewaretoken: csrf,
                },
                success: function (response) {
                    chooseValidationColor('#id_username', response.emailStatus);
                    if (response.emailStatus === 'success') {
                        required.email = true;
                    } else if (response.emailStatus === 'error') {
                        required.email = true;
                        showMessage(response.emailError);
                    }
                }
            });
            email = $(this).val();
        }
        checkBtnRegister(required);
    });

    $('#btn-register').click(function () {
        $.ajax({
            url: '',
            type: 'post',
            data: {
                id: $(this).id,
                username: $('#id_username').value,
                pass1: $('#id_password1').val(),
                pass2: $('#id_password2').val(),
                email: $('#id_email').val(),
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