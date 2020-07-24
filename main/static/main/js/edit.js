$(function () {
    const body = $('body');
    const csrf = $('input[name="csrfmiddlewaretoken"]').val();
    const timeShow = 300;

    let username = $('#username');
    let passwordOld = $('#password_old');
    let password1 = $('#password1');
    let password2 = $('#password2');
    let email = $('#email');
    let name = $('#name');
    let surname = $('#surname');
    let patronymic = $('#patronymic');
    let birthdate = $('#birthdate');

    let btnName = $('#btnName');
    let btnPassword = $('#btnPassword');
    let btnBirthdate = $('#btnBirthdate');
    let btnUsername = $('#btnUsername');
    let btnEmail = $('#btnEmail');

    let infoName = $('.info__name');
    let aCompany = $('.info__company');
    let addPosition = $('.position__substrate');
    let addPlatform = $('.platform__substrate');
    let menuPosition = addPosition.children('._hint-down-click').children('._hint-down-block').children('.menu');
    let menuPlatform = addPlatform.children('._hint-down-click').children('._hint-down-block').children('.menu');
    let openAdd;

    let required = {
        'username': false,
        'password_old': false,
        'password1': false,
        'password2': false,
        'email': false,
        'name': false,
        'surname': false,
        'patronymic': false,
        'birthdate': false,
    };

    let errors = {
        'username': false,
        'password_old': false,
        'password1': false,
        'password2': false,
        'email': false,
        'name': false,
        'surname': false,
        'patronymic': false,
        'birthdate': false,
    };

    // Расположеие ссылки на компанию возле имени
    $(function () {
        if (parseFloat(infoName.width()) + parseFloat(infoName.css('margin-left')) + parseFloat(infoName.css('margin-right')) + 30 + parseFloat(aCompany.width()) <= 680) {
            aCompany.css({
                'position': 'absolute',
                'right': '0',
                'bottom': 'calc(100% + 14px)'
            })
        }
        aCompany.removeClass('hide')
    });

    // Кастомный календарь
    if (birthdate.prop('type') !== 'date') {
        birthdate.datepicker({
            onSelect: function (formattedDate, date, inst) {
                ajaxForInput(birthdate, btnBirthdate, {
                    'birthdate': formattedDate,
                });
                // let el = birthdate;
                // $.ajax({
                //     url: '/edit/check_input/birthdate',
                //     type: 'post',
                //     data: {
                //         id: birthdate[0].id,
                //         birthday: formattedDate,
                //         csrfmiddlewaretoken: csrf,
                //     },
                //     success: function (response) {
                //         chooseValidationColor($('#id_birthday')[0], response.resultStatus);
                //         if (response.resultStatus === 'success') {
                //             required.birthdate = true;
                //             errors.birthdate = false;
                //             removeErrors(el);
                //         } else if (response.resultStatus === 'error') {
                //             required.birthdate = false;
                //             errors.birthdate = true;
                //             showErrors(el, response.resultError);
                //         }
                //         checkBtnPost(btnBirthdate, birthdate);
                //     },
                //     error: function () {
                //         console.log('Что - то пошло не так :(');
                //     },
                // });
            },
        });
    }

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
    body.on('input', '#username', function () {
        $(this).val($(this).val().toLowerCase());
        let elem = $(this);
        ajaxForInput(elem, btnUsername, {
            'username': elem.val(),
        });
    });

    body.on('input', '#password_old', function () {
        let elem = $(this);
        ajaxForInput(elem, btnPassword, {
            'password_old': elem.val(),
        });
    });

    body.on('input', '#password1', function () {
        let elem = $(this);
        ajaxForInput(elem, btnPassword, {
            'password1': elem.val(),
        });
    });

    body.on('input', '#password2', function () {
        let elem = $(this);
        ajaxForInput(elem, btnPassword, {
            'password1': elem.val(),
            'password2': password2.val(),
        });
    });

    body.on('input', '#email', function () {
        let elem = $(this);
        ajaxForInput(elem, btnEmail, {
            'email': elem.val(),
        });
    });

    body.on('input', '#name', function () {
        let elem = $(this);
        ajaxForInput(elem, btnName, {
            'name': elem.val(),
        });
    });

    body.on('input', '#surname', function () {
        let elem = $(this);
        ajaxForInput(elem, btnName, {
            'surname': elem.val(),
        });
    });

    body.on('input', '#patronymic', function () {
        let elem = $(this);
        ajaxForInput(elem, btnName, {
            'patronymic': elem.val(),
        });
    });

    body.on('input', '#birthdate', function () {
        let elem = $(this);
        ajaxForInput(elem, btnBirthdate, {
            'birthdate': elem.val(),
        });
    });

    // Сохранение изменений
    body.on('click', '.button-save', function () {
        let partUrl = $(this).attr('data-part-url');
        let values;
        if (partUrl === 'name') {
            values = {
                name: name.val(),
                surname: surname.val(),
                patronymic: patronymic.val(),
            }
        } else if (partUrl === 'birthdate') {
            values = {
                birthdate: birthdate.val(),
            }
        } else if (partUrl === 'email') {
            values = {
                email: email.val(),
            }
        } else if (partUrl === 'username') {
            values = {
                username: username.val(),
            }
        } else if (partUrl === 'password') {
            values = {
                password_old: passwordOld.val(),
                password1: password1.val(),
                password2: password2.val(),
            }
        } else {
            throw new Error('Unexpected argument values');
        }
        $.ajax({
            url: `edit/save/${partUrl}`,
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
                values: values,
            },
            success: function (response) {
                if (partUrl === 'name') {

                } else if (partUrl === 'birthdate') {

                } else if (partUrl === 'email') {

                } else if (partUrl === 'username') {

                } else if (partUrl === 'password') {
                    if (response.resultStatus === 'error') {
                        chooseValidationColor(passwordOld, response.resultStatus);
                        passwordOld.val('');
                        password1.val('');
                        password2.val('');
                        btnPassword.prop({
                            'disabled': true,
                        });
                        showErrors(passwordOld, response.listErrors);
                    }
                } else {
                    throw new Error('Unexpected argument values');
                }
            },
            statusCode: {
                400: function () {
                    console.log('Error 400 - Некорректный запрос');
                },
                403: function () {
                    console.log('Error 403 - Доступ запрещён');
                },
                404: function () {
                    console.log('Error 404 - Страница не найдена');
                },
                500: function () {
                    console.log('Error 500 - Внутренняя ошибка сервера');
                }
            },
            error: function () {
                console.log('Что - то пошло не так :(');
            }
        })
    });

    // Раскрытие/скрытие настроек
    body.on('click', '.setting__edit', function () {
        let setting = $(this.closest('.setting'));
        let settingClose = setting.children('.setting__close');
        let settingOpen = setting.children('.setting__open');
        if (settingClose.hasClass('show') && settingOpen.hasClass('hide')) {
            settingClose.removeClass('show');
            settingClose.addClass('hide');
            settingOpen.removeClass('hide');
            settingOpen.addClass('show');
        } else if (settingClose.hasClass('hide') && settingOpen.hasClass('show')) {
            settingOpen.removeClass('show');
            settingOpen.addClass('hide');
            settingClose.removeClass('hide');
            settingClose.addClass('show');
        } else {
            throw new Error('Invalid attributes');
        }
    });

    // Открыть меню (Добавить)
    body.on('click', '._hint-up-click', function () {
        let addUp = $(this.closest('._hint-click'));
        let addDown = $(addUp).children('._hint-down-click');
        addUp.toggleClass('active');
        addDown.toggle();
        openAdd = $(this).parent();
    });

    // Скрыть меню (Добавить)
    $(window).on('mouseup', function (el) {
        let _ = openAdd;
        if ($(_).children('._hint-down-click').css('display') !== 'none') {
            if (el.target.closest('._hint-up-click') !== null &&
                (el.target.closest('.position__add') !== null && ($(_).children('._hint-up-click')).hasClass('position__add')) ||
                (el.target.closest('.platform__add') !== null && ($(_).children('._hint-up-click')).hasClass('platform__add'))) {
            } else if (el.target.closest('._hint-down-click') === null || el.target.classList.contains('item__block')) {
                $(_).toggleClass('active');
                $(_).children('._hint-down-click').toggle();
            }
        }
    });

    // Добавление должностей и отделов
    body.on('click', '.item__block', function (el) {
        let typeSubstrate = el.target.closest('._hint-click');
        let type;
        let name = $(this).attr('data-name');
        let id = $(this).attr('data-id');
        if ($(typeSubstrate).hasClass('platform__substrate')) {
            type = 'platform';
        } else if ($(typeSubstrate).hasClass('position__substrate')) {
            type = 'position';
        }

        $.ajax({
            url: `/edit/${type}/add/${id}`,
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
                type: type,
                id: id,
                name: name, // На всякий случай
            },
            success: function (response) {
                let newEl = document.createElement('div');
                newEl.classList.add(type);
                $(newEl).attr({
                    'data-name': name,
                    'data-id': id,
                });
                let role = document.createElement('div');
                role.classList.add('role');
                role.innerText = name;
                let remove = document.createElement('div');
                let removeClassList = remove.classList;
                removeClassList.add(`${type}__remove`);
                removeClassList.add('remove-item');
                let cross = document.createElement('div');
                cross.classList.add('cross-in-circle');
                let circle = document.createElement('div');
                circle.classList.add('circle');
                let line1 = document.createElement('div');
                line1.classList.add('line-1');
                let line2 = document.createElement('div');
                line2.classList.add('line-2');
                newEl.prepend(role);
                role.prepend(remove);
                remove.prepend(cross);
                cross.prepend(circle);
                circle.prepend(line1);
                line1.prepend(line2);
                $(typeSubstrate).before(newEl);
                $(el.target).parent().remove();
                if ((type === 'platform' && menuPlatform.children('.menu__item').length < 1) || (type === 'position' && menuPosition.children('.menu__item').length < 1)) {
                    $(typeSubstrate).addClass('hide');
                }
            },
            statusCode: {
                400: function () {
                    console.log('Error 400 - Некорректный запрос');
                },
                403: function () {
                    console.log('Error 403 - Доступ запрещён');
                },
                404: function () {
                    console.log('Error 404 - Страница не найдена');
                },
                500: function () {
                    console.log('Error 500 - Внутренняя ошибка сервера');
                }
            },
            error: function () {
                console.log('Что - то пошло не так :(');
            }
        });
    });

    // Удаление должностей и отделов
    body.on('click', '.remove-item', function () {
        let type;
        if ($(this).hasClass('platform__remove')) {
            type = 'platform';
        } else if ($(this).hasClass('position__remove')) {
            type = 'position';
        } else {
            throw new Error('Unexpected values');
        }
        let el = $(this).parent().parent();
        let name = el.attr('data-name');
        let id = el.attr('data-id');

        $.ajax({
            url: `/edit/${type}/remove/${id}`,
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
                type: type,
                id: id,
                name: name, // На всякий случай
            },
            success: function (response) {
                if (type === 'position' && menuPosition.children('.menu__item').length < 1) {
                    addPosition.removeClass('hide');
                } else if (type === 'platform' && menuPlatform.children('.menu__item').length < 1) {
                    addPlatform.removeClass('hide');
                }
                let newItem = document.createElement('div');
                newItem.classList.add('menu__item');
                let itemBlock = document.createElement('div');
                itemBlock.classList.add('item__block');
                $(itemBlock).attr({
                    'data-name': name,
                    'data-id': id,
                });
                itemBlock.innerText = name;
                let itemLine = document.createElement('div');
                itemLine.classList.add('item__line');
                newItem.prepend(itemLine);
                newItem.prepend(itemBlock);
                if (type === 'platform') {
                    menuPlatform.prepend(newItem);
                } else if (type === 'position') {
                    menuPosition.prepend(newItem);
                } else {
                    throw new Error('Unexpected values');
                }
                el.remove();
            },
            statusCode: {
                400: function () {
                    console.log('Error 400 - Некорректный запрос');
                },
                403: function () {
                    console.log('Error 403 - Доступ запрещён');
                },
                404: function () {
                    console.log('Error 404 - Страница не найдена');
                },
                500: function () {
                    console.log('Error 500 - Внутренняя ошибка сервера');
                }
            },
            error: function () {
                console.log('Что - то пошло не так :(');
            }
        })
    });

    // // Удаление должностей
    // body.on('click', '.position__remove', function () {
    //     if (menuPosition.children('.menu__item').length < 1) {
    //         addPosition.removeClass('hide');
    //     }
    //     let position = $(this).parent().parent();
    //     let positionName = position.attr('data-name');
    //     let positionId = position.attr('data-id');
    //     let newItem = document.createElement('div');
    //     newItem.classList.add('menu__item');
    //     let itemBlock = document.createElement('div');
    //     itemBlock.classList.add('item__block');
    //     $(itemBlock).attr({
    //         'data-name': positionName,
    //         'data-id': positionId,
    //     });
    //     itemBlock.innerText = positionName;
    //     let itemLine = document.createElement('div');
    //     itemLine.classList.add('item__line');
    //     newItem.prepend(itemLine);
    //     newItem.prepend(itemBlock);
    //     menuPosition.prepend(newItem);
    //     position.remove();
    // });
    //
    // // Удаление отделов
    // body.on('click', '.platform__remove', function () {
    //     if (menuPlatform.children('.menu__item').length < 1) {
    //         addPlatform.removeClass('hide');
    //     }
    //     let platform = $(this).parent().parent();
    //     let platformName = platform.attr('data-name');
    //     let platformId = platform.attr('data-id');
    //     let newItem = document.createElement('div');
    //     newItem.classList.add('menu__item');
    //     let itemBlock = document.createElement('div');
    //     itemBlock.classList.add('item__block');
    //     $(itemBlock).attr({
    //         'data-name': platformName,
    //         'data-id': platformId,
    //     });
    //     itemBlock.innerText = platformName;
    //     let itemLine = document.createElement('div');
    //     itemLine.classList.add('item__line');
    //     newItem.prepend(itemLine);
    //     newItem.prepend(itemBlock);
    //     menuPlatform.prepend(newItem);
    //     platform.remove();
    // });


    // functions

    // Окраска поля при ошибке
    function chooseValidationColor(element, status) {
        if (status === 'success') {
            if (element.classList.contains('error')) {
                element.classList.remove('error');
            }
        } else if (status === 'error') {
            element.classList.add('error');
        }
    }

    // Удаление ошибок
    function removeErrors(el) {
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

    // Появление ошибок
    function showErrors(el, listErrors) {
        // console.log(listErrors)
        let popup = $(el).parent().children('.popup');
        let alert = popup.children('.popup_message');
        alert.children().remove();
        for (let i = 0; i < listErrors.length; i++) {
            let span = document.createElement('span');
            span.classList.add('popup_message-text');
            span.textContent = listErrors[i];
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

    // Можно ли нажать на кнопку сохранения изменений
    function checkBtnPost(btn, elem) {
        let idElem = elem.prop('id');
        if (idElem === 'name' || idElem === 'surname' || idElem === 'patronymic') {
            checkBtnName(btn);
        } else if (idElem === 'birthdate') {
            checkBtnBirthdate(btn);
        } else if (idElem === 'email') {
            checkBtnEmail(btn);
        } else if (idElem === 'username') {
            checkBtnUsername(btn);
        } else if (idElem === 'password_old' || idElem === 'password1' || idElem === 'password2') {
            checkBtnPassword(btn);
        } else {
            throw new Error('Unexpected values');
        }
    }

    function checkBtnName(btn) {
        if (required.name || required.surname || required.patronymic) {
            btn.prop({'disabled': false});
        } else {
            btn.prop({'disabled': true});
        }
    }

    function checkBtnBirthdate(btn) {
        if (required.birthdate) {
            btn.prop({'disabled': false});
        } else {
            btn.prop({'disabled': true});
        }
    }

    function checkBtnEmail(btn) {
        if (required.email) {
            btn.prop({'disabled': false});
        } else {
            btn.prop({'disabled': true});
        }
    }

    function checkBtnUsername(btn) {
        if (required.username) {
            btn.prop({'disabled': false});
        } else {
            btn.prop({'disabled': true});
        }
    }

    function checkBtnPassword(btn) {
        if (required.password1 && required.password2) {
            btn.prop({'disabled': false});
        } else {
            btn.prop({'disabled': true});
        }
    }

    // Первая буква заглавная, остальные строчные
    function formatValue(el) {
        let element = el[0];
        if (element.value !== '') {
            let position = element.selectionStart;
            element.value = element.value[0].toUpperCase() + element.value.slice(1).toLowerCase();
            element.selectionStart = element.selectionEnd = position;
        }
    }

    function ajaxForInput(elem, btn, values) {
        let id = elem[0].id;
        $.ajax({
            url: `/edit/check_input/${id}`,
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
                id: id,  // При разных url не нужен
                values: values,
            },
            success: function (response) {
                chooseValidationColor(elem[0], response.resultStatus);
                if (id === 'name') {
                    if (response.resultStatus === 'success') {
                        required.name = true;
                        errors.name = false;
                        removeErrors(elem);
                    } else if (response.resultStatus === 'error') {
                        required.name = false;
                        errors.name = true;
                        showErrors(elem, response.resultError);
                    }
                } else if (id === 'surname') {
                    if (response.resultStatus === 'success') {
                        required.surname = true;
                        errors.surname = false;
                        removeErrors(elem);
                    } else if (response.resultStatus === 'error') {
                        required.surname = false;
                        errors.surname = true;
                        showErrors(elem, response.resultError);
                    }
                } else if (id === 'patronymic') {
                    if (response.resultStatus === 'success') {
                        required.patronymic = true;
                        errors.patronymic = false;
                        removeErrors(elem);
                    } else if (response.resultStatus === 'error') {
                        required.patronymic = false;
                        errors.patronymic = true;
                        showErrors(elem, response.resultError);
                    }
                } else if (id === 'birthdate') {
                    if (response.resultStatus === 'success') {
                        required.birthdate = true;
                        errors.birthdate = false;
                        removeErrors(elem);
                    } else if (response.resultStatus === 'error') {
                        required.birthdate = false;
                        errors.birthdate = true;
                        showErrors(elem, response.resultError);
                    }
                } else if (id === 'email') {
                    if (response.resultStatus === 'success') {
                        required.email = true;
                        errors.email = false;
                        removeErrors(elem);
                    } else if (response.resultStatus === 'error') {
                        required.email = false;
                        errors.email = true;
                        showErrors(elem, response.resultError);
                    }
                } else if (id === 'username') {
                    if (response.resultStatus === 'success') {
                        required.username = true;
                        errors.username = false;
                        removeErrors(elem);
                    } else if (response.resultStatus === 'error') {
                        required.username = false;
                        errors.username = true;
                        showErrors(elem, response.resultError);
                    }
                } else if (id === 'password_old') {
                    if (response.resultStatus === 'success') {
                        required.password_old = true;
                        errors.password_old = false;
                        removeErrors(elem);
                    } else if (response.resultStatus === 'error') {
                        required.password_old = false;
                        errors.password_old = true;
                        showErrors(elem, response.resultError);
                    }
                } else if (id === 'password1') {
                    if (response.resultStatus === 'success') {
                        required.password1 = true;
                        errors.password1 = false;
                        removeErrors(elem);
                        $('#password2').prop({
                            'disabled': false,
                        });
                    } else if (response.resultStatus === 'error') {
                        required.password1 = false;
                        errors.password1 = true;
                        showErrors(elem, response.resultError);
                        $('#password2').prop({
                            'disabled': true,
                        });
                    }
                } else if (id === 'password2') {
                    if (response.resultStatus === 'success') {
                        required.password2 = true;
                        errors.password2 = false;
                        removeErrors(elem);
                    } else if (response.resultStatus === 'error') {
                        required.password2 = false;
                        errors.password2 = true;
                        showErrors(elem, response.resultError);
                    }
                } else {
                    throw new Error('Unexpected values');
                }
                checkBtnPost(btn, elem)
            },
            error: function () {
                console.log('Что - то пошло не так! :(');
            },
        });
    }

});


// function ajaxForUsername(el, csrf, required, errors, body, timeShow) {
//     el[0].value = el[0].value.toLowerCase();
//     $.ajax({
//         url: '',
//         type: 'post',
//         data: {
//             id: el[0].id,
//             username: el[0].value,
//             csrfmiddlewaretoken: csrf,
//         },
//         success: function (response) {
//             chooseValidationColor(el[0], response.resultStatus);
//             if (response.resultStatus === 'success') {
//                 required.username = true;
//                 errors.username = false;
//                 removeErrors(el, timeShow);
//             } else if (response.resultStatus === 'error') {
//                 required.username = false;
//                 errors.username = true;
//                 showErrors(body, el, response.resultError, timeShow);
//             }
//             checkBtnRegister(required);
//             checkBtnNext(required);
//         },
//         error: function () {
//             console.log('Что - то пошло не так :(');
//         },
//     });
// }
//
// function ajaxForPassword1(el, csrf, required, errors, body, timeShow) {
//     $.ajax({
//         url: '',
//         type: 'post',
//         data: {
//             id: el[0].id,
//             password1: el[0].value,
//             csrfmiddlewaretoken: csrf,
//         },
//         success: function (response) {
//             chooseValidationColor(el[0], response.resultStatus);
//             if (response.resultStatus === 'success') {
//                 required.password1 = true;
//                 errors.password1 = false;
//                 removeErrors(el, timeShow);
//                 $('#id_password2').prop({
//                     'disabled': false,
//                 });
//             } else if (response.resultStatus === 'error') {
//                 required.password1 = false;
//                 errors.password1 = true;
//                 showErrors(body, el, response.resultError, timeShow);
//                 $('#id_password2').prop({
//                     'disabled': true,
//                 });
//             }
//             checkBtnRegister(required);
//             checkBtnNext(required);
//         },
//         error: function () {
//             console.log('Что - то пошло не так :(');
//         },
//     });
// }
//
// function ajaxForPassword2(el, csrf, required, errors, body, timeShow) {
//     let pass1 = $('#id_password1');
//     $.ajax({
//         url: '',
//         type: 'post',
//         data: {
//             id: el[0].id,
//             password1: pass1[0].value,
//             password2: el[0].value,
//             csrfmiddlewaretoken: csrf,
//         },
//         success: function (response) {
//             chooseValidationColor(el[0], response.resultStatus);
//             if (response.resultStatus === 'success') {
//                 required.password2 = true;
//                 errors.password2 = false;
//                 removeErrors(el, timeShow);
//             } else if (response.resultStatus === 'error') {
//                 required.password2 = false;
//                 errors.password2 = true;
//                 showErrors(body, el, response.resultError, timeShow);
//             }
//             checkBtnRegister(required);
//             checkBtnNext(required);
//         },
//         error: function () {
//             console.log('Что - то пошло не так :(');
//         },
//     });
// }
//
// function ajaxForEmail(el, csrf, required, errors, body, timeShow) {
//     $.ajax({
//         url: '',
//         type: 'post',
//         data: {
//             id: el[0].id,
//             email: el[0].value,
//             csrfmiddlewaretoken: csrf,
//         },
//         success: function (response) {
//             chooseValidationColor(el[0], response.resultStatus);
//             if (response.resultStatus === 'success') {
//                 required.email = true;
//                 errors.email = false;
//                 removeErrors(el, timeShow);
//             } else if (response.resultStatus === 'error') {
//                 required.email = false;
//                 errors.email = true;
//                 showErrors(body, el, response.resultError, timeShow);
//             }
//             checkBtnRegister(required);
//             checkBtnNext(required);
//         },
//         error: function () {
//             console.log('Что - то пошло не так :(');
//         },
//     });
// }
//
// function ajaxForName(el, csrf, required, errors, body, timeShow) {
//     formatValue(el);
//     $.ajax({
//         url: '',
//         type: 'post',
//         data: {
//             id: el[0].id,
//             name: el[0].value,
//             csrfmiddlewaretoken: csrf,
//         },
//         success: function (response) {
//             chooseValidationColor(el[0], response.resultStatus);
//             if (response.resultStatus === 'success') {
//                 required.name = true;
//                 errors.name = false;
//                 removeErrors(el, timeShow);
//             } else if (response.resultStatus === 'error') {
//                 required.name = false;
//                 errors.name = true;
//                 showErrors(body, el, response.resultError, timeShow);
//             }
//             checkBtnRegister(required);
//             // checkBtnNext(required);
//         },
//         error: function () {
//             console.log('Что - то пошло не так :(');
//         },
//     });
// }
//
// function ajaxForSurname(el, csrf, required, errors, body, timeShow) {
//     formatValue(el);
//     $.ajax({
//         url: '',
//         type: 'post',
//         data: {
//             id: el[0].id,
//             surname: el[0].value,
//             csrfmiddlewaretoken: csrf,
//         },
//         success: function (response) {
//             chooseValidationColor(el[0], response.resultStatus);
//             if (response.resultStatus === 'success') {
//                 required.surname = true;
//                 errors.surname = false;
//                 removeErrors(el, timeShow);
//             } else if (response.resultStatus === 'error') {
//                 required.surname = false;
//                 errors.surname = true;
//                 showErrors(body, el, response.resultError, timeShow);
//             }
//             checkBtnRegister(required);
//             // checkBtnNext(required);
//         },
//         error: function () {
//             console.log('Что - то пошло не так :(');
//         },
//     });
// }
//
// function ajaxForPatronymic(el, csrf, required, errors, body, timeShow) {
//     formatValue(el);
//     $.ajax({
//         url: '',
//         type: 'post',
//         data: {
//             id: el[0].id,
//             patronymic: el[0].value,
//             csrfmiddlewaretoken: csrf,
//         },
//         success: function (response) {
//             chooseValidationColor(el[0], response.resultStatus);
//             if (response.resultStatus === 'success') {
//                 required.patronymic = true;
//                 errors.patronymic = false;
//                 removeErrors(el, timeShow);
//             } else if (response.resultStatus === 'error') {
//                 required.patronymic = false;
//                 errors.patronymic = true;
//                 showErrors(body, el, response.resultError, timeShow);
//             }
//             checkBtnRegister(required);
//             // checkBtnNext(required);
//         },
//         error: function () {
//             console.log('Что - то пошло не так :(');
//         },
//     });
// }
//
// function ajaxForBirthday(el, csrf, required, errors, body, timeShow) {
//     $.ajax({
//         url: '',
//         type: 'post',
//         data: {
//             id: el[0].id,
//             birthday: el[0].value,
//             csrfmiddlewaretoken: csrf,
//         },
//         success: function (response) {
//             chooseValidationColor(el[0], response.resultStatus);
//             if (response.resultStatus === 'success') {
//                 required.birthday = true;
//                 errors.birthday = false;
//                 removeErrors(el, timeShow);
//             } else if (response.resultStatus === 'error') {
//                 required.birthday = false;
//                 errors.birthday = true;
//                 showErrors(body, el, response.resultError, timeShow);
//             }
//             checkBtnRegister(required);
//             // checkBtnNext(required);
//         },
//         error: function () {
//             console.log('Что - то пошло не так :(');
//         },
//     });
// }