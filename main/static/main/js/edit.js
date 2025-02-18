$(function () {
    const body = $('body');
    const csrf = $('input[name="csrfmiddlewaretoken"]').val();
    const timeShow = 300;

    const colCenter = $('.col-center');
    const modal = $('.modal');
    const emailCode = $('#email_code');
    const modalSuccess = $('#modal_success');
    let photo = $('.left-content__photo');
    let updPhoto = $('.upd-photo');
    let headPhoto = $('.head-menu-img');

    let username = $('#username');
    let passwordOld = $('#password_old');
    let password1 = $('#password1');
    let password2 = $('#password2');
    let email = $('#email');
    let passwordForEmail = $('#password_for_email');
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
        'password_for_email': false,
        'email_code': false,
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
        'password_for_email': false,
        'email_code': false,
        'name': false,
        'surname': false,
        'patronymic': false,
        'birthdate': false,
    };

    // Расположение ссылки на команду
    positionCompany();

    // Кастомный календарь
    if (birthdate.prop('type') !== 'date') {
        birthdate.datepicker({
            onSelect: function (formattedDate, date, inst) {
                ajaxForInput(birthdate, btnBirthdate, {
                    'birthdate': formattedDate,
                });
            },
            dateFormat: 'd.m.yyyy',
            position: 'top left',
        });
    }

    body.on('click', '.left-content__delete-photo', function (event) {
        event.preventDefault();
        $.ajax({
            url: 'edit/photo/delete',
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
            },
            success: function (response) {
                // console.log(response.new_photo_url)
                $(photo).attr({
                    'src': response.new_photo_url,
                    // 'src': "../image/photo.svg",
                });
                $(headPhoto).attr({
                    'src': response.new_photo_url,
                });
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

    body.on('click', '.left-content__update-photo', function (event) {
        event.preventDefault();
        $(updPhoto).trigger('click');
    });

    // Обновление фото
    body.on('change', '.upd-photo', function () {
        let files = this.files;
        // console.log(files)
        // ничего не делаем если files пустой
        if (typeof files == 'undefined') return;
        // создадим объект данных формы
        let data = new FormData();
        // заполняем объект данных файлами в подходящем для отправки формате
        $.each(files, function (key, value) {
            data.append(key, value);
        });
        // console.log(data)
        $.ajax({
            url: 'edit/photo/update',
            type: 'post',
            data: data,
            cache: false,
            // отключаем обработку передаваемых данных, пусть передаются как есть
            processData: false,
            // отключаем установку заголовка типа запроса. Так jQuery скажет серверу что это строковой запрос
            contentType: false,
            success: function (response) {
                // console.log(response.new_photo_url)
                $(photo).attr({
                    'src': response.new_photo_url,
                });
                $(headPhoto).attr({
                    'src': response.new_photo_url,
                });
            },
            statusCode: {
                400: function () {
                    // throw new Error('Error 400 - Некорректный запрос');
                },
                403: function () {
                    // throw new Error('Error 403 - Доступ запрещён');
                },
                413: function () {
                    Snackbar.show({
                        text: `Размер загружаемого фото слишком большой`,
                        textColor: '#ff0000',
                        customClass: 'custom center',
                        showAction: false,
                        duration: 3000,
                    });
                },
                404: function () {
                    // throw new Error('Error 404 - Страница не найдена');
                },
                500: function () {
                    // throw new Error('Error 500 - Внутренняя ошибка сервера');
                }
            },
            error: function () {
                // throw new Error('Что - то пошло не так :(');
            }
        });

        // $.ajax({
        //     url: 'edit/photo/update',
        //     type: 'post',
        //     data: {
        //         new_photo: file,
        //         csrfmiddlewaretoken: csrf,
        //     },
        //     success: function (response) {
        //         $(photo).attr({
        //             'src': response.new_photo_url,
        //         })
        //     },
        //     statusCode: {
        //         400: function () {
        //             console.log('Error 400 - Некорректный запрос');
        //         },
        //         403: function () {
        //             console.log('Error 403 - Доступ запрещён');
        //         },
        //         404: function () {
        //             console.log('Error 404 - Страница не найдена');
        //         },
        //         500: function () {
        //             console.log('Error 500 - Внутренняя ошибка сервера');
        //         }
        //     },
        //     error: function () {
        //         console.log('Что - то пошло не так :(');
        //     }
        // });
    });

    // Закрытие модального окна
    body.on('click', '.modal', function (el) {
        if ($(el.target).hasClass('modal') || el.target.id === 'modal_close') {
            sessionStorage.removeItem('new_email');
            modal.toggleClass('hide');
        }
    });

    // // Обработака поля в модальном окне
    // body.on('input', '#email_code', function (el) {
    //     if (el.target.value.length > 0) {
    //         modalSuccess.prop({
    //             disabled: false,
    //         })
    //     } else {
    //         modalSuccess.prop({
    //             disabled: true,
    //         })
    //     }
    // });

    // Вывод шибки при фокусе на поле
    body.on('focus', '.input-field', function () {
        let name = $(this)[0].id;
        for (let key in errors) {
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

    body.on('input', '.input-field', function (el) {
        let id = $(this)[0].id;
        // console.log(id)
        if (id === 'password_old' || id === 'password_for_email') {
            let popup = $(this).parent().children('.popup');
            popup.addClass('old');
            $(this).removeClass('error');
            popup.stop().animate({
                opacity: 0,
            }, timeShow, function () {
                $(this).remove();
            });
            if (id === 'password_old') {
                errors.password_old = false;
            } else if (id === 'password_for_email') {
                errors.password_for_email = false;
            }
        }
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
            'password_old': passwordOld.val(), // Теперь не нужно
            'password1': elem.val(),
            'password2': password2.val(),
        });
    });

    body.on('input', '#password2', function () {
        let elem = $(this);
        ajaxForInput(elem, btnPassword, {
            'password1': password1.val(),
            'password2': elem.val(),
        });
    });

    body.on('input', '#email', function () {
        let elem = $(this);
        ajaxForInput(elem, btnEmail, {
            'email': elem.val(),
        });
    });

    body.on('input', '#password_for_email', function () {
        let elem = $(this);
        ajaxForInput(elem, btnEmail, {
            'password_for_email': elem.val(),
        });
    });

    body.on('input', '#email_code', function () {
        let elem = $(this);
        ajaxForInput(elem, modalSuccess, {
            'email_code': elem.val(),
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
    body.on('click', '.button-save', function (elem) {
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
                password_for_email: passwordForEmail.val(),
                host: location.hostname,
            }
        } else if (partUrl === 'email_code') {
            values = {
                email: sessionStorage.getItem('new_email'),
                email_code: emailCode.val(),
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
                $(elem.target).prop({'disabled': true});
                let currentSetting = $(elem.target).parent();
                let spanMax = currentSetting.children('.setting__substrate').children('.setting__value');
                let spanMin = currentSetting.parent().parent().parent().children('.setting__close')
                    .children('.setting__mini').children('.setting__2-block')
                    .children('.setting__value');
                if (partUrl === 'email_code') {
                    let setting = $('.setting__email');
                    spanMax = $(setting[1]);
                    spanMin = $(setting[0]);
                }
                if (partUrl === 'name') {
                    name.val(response.name);
                    surname.val(response.surname);
                    patronymic.val(response.patronymic);
                    infoName.text(`${response.name} ${response.surname}`);
                    positionCompany();
                    spanMax.text(`${response.surname} ${response.name} ${response.patronymic}`);
                    spanMin.text(`${response.surname} ${response.name} ${response.patronymic}`);
                    $('.head-menu-name').text(`${response.name} ${response.surname}`);
                    required.name = false;
                    required.surname = false;
                    required.patronymic = false;
                    errors.name = false;
                    errors.surname = false;
                    errors.patronymic = false;
                } else if (partUrl === 'birthdate') {
                    birthdate.val(response.birthdate.date);
                    spanMax.text(`${response.birthdate.text}`);
                    spanMin.text(`${response.birthdate.text}`);
                    required.birthdate = false;
                    errors.birthdate = false;
                } else if (partUrl === 'email') {
                    passwordForEmail.val('');
                    required.password_for_email = false;
                    errors.password_for_email = false;
                    if (response.resultStatus === 'error') {
                        required.email = true;
                        errors.email = false;
                        errors.password_for_email = true;
                        chooseValidationColor(passwordForEmail[0], response.resultStatus, response.listErrors.password_for_email);
                        showErrors(passwordForEmail, response.listErrors.password_for_email);
                        passwordForEmail.focus();
                    } else if (response.resultStatus === 'success') {
                        required.email = false;
                        errors.email = false;
                        sessionStorage.setItem('new_email', email.val());
                        email.val('');
                        // console.log('show')
                        modal.toggleClass('hide');
                        delete values['password_for_email'];
                        $.ajax({
                            url: 'edit/save/email/send_mail',
                            type: 'post',
                            data: {
                                csrfmiddlewaretoken: csrf,
                                values: values,
                                host: location.hostname,
                            },
                            success: function () {
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
                } else if (partUrl === 'email_code') {
                    if (response.resultStatus === 'error') {
                        errors.email_code = true;
                        chooseValidationColor(emailCode[0], response.resultStatus, response.listErrors);
                        showErrors(emailCode, response.listErrors);
                        passwordForEmail.focus();
                    } else if (response.resultStatus === 'success') {
                        spanMax.text(`${response.email}`);
                        spanMin.text(`${response.email}`);
                        sessionStorage.removeItem('new_email');
                        modal.toggleClass('hide');
                    }
                } else if (partUrl === 'username') {
                    email.val(response.username);
                    spanMax.text(`${response.username}`);
                    spanMin.text(`${response.username}`);
                    required.username = false;
                    errors.username = false;
                } else if (partUrl === 'password') {
                    passwordOld.val('');
                    password1.val('');
                    password2.val('');
                    password2.prop({
                        'disabled': true,
                    });
                    required.password_old = false;
                    required.password1 = false;
                    required.password2 = false;
                    errors.password_old = false;
                    errors.password1 = false;
                    errors.password2 = false;
                    if (response.resultStatus === 'error') {
                        errors.password_old = true;
                        chooseValidationColor(passwordOld[0], response.resultStatus, response.listErrors.old_password);
                        showErrors(passwordOld, response.listErrors.old_password);
                        passwordOld.focus();
                    }
                } else {
                    throw new Error('Unexpected argument values');
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
                $(typeSubstrate).before(getNewRoundedStrip(type, name, id));
                $(typeSubstrate).parent().children('.empty').addClass('hide');
                $(el.target).parent().remove();
                if ((type === 'platform' && menuPlatform.children('.menu__item').length < 1) || (type === 'position' && menuPosition.children('.menu__item').length < 1)) {
                    $(typeSubstrate).addClass('hide');
                }
            },
            error: function () {
            }
        });
    });

    /**
     * Получить новый элемент для должности или отдела
     *
     * @param {string} type
     * @param {string} name
     * @param {string, int} id
     * @returns {HTMLDivElement}
     */
    function getNewRoundedStrip(type, name, id) {
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
        return newEl;
    }

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
                if (el.parent().children('.platform, .position').length === 1) {
                    el.parent().children('.empty').removeClass('hide');
                }
                el.remove();
            },
            error: function () {
            }
        })
    });

    // functions

    // Окраска поля при ошибке
    function chooseValidationColor(element, status, listErrors) {
        if (status === 'success' || listErrors.length < 1) {
            if (element.classList.contains('error')) {
                element.classList.remove('error');
            }
        } else if (status === 'error' && listErrors.length > 0) {
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
        if (listErrors.length > 0) {
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
        } else {
            removeErrors(el);
        }
    }

    // Можно ли нажать на кнопку сохранения изменений
    function checkBtnPost(btn, elem) {
        let idElem = elem.prop('id');
        if (idElem === 'name' || idElem === 'surname' || idElem === 'patronymic') {
            checkBtnName(btn);
        } else if (idElem === 'birthdate') {
            checkBtnBirthdate(btn);
        } else if (idElem === 'email' || idElem === 'password_for_email') {
            checkBtnEmail(btn);
        } else if (idElem === 'email_code') {
            checkBtnEmailCode(btn);
        } else if (idElem === 'username') {
            checkBtnUsername(btn);
        } else if (idElem === 'password_old' || idElem === 'password1' || idElem === 'password2') {
            checkBtnPassword(btn);
        } else {
            throw new Error('Unexpected values');
        }
    }

    function checkBtnName(btn) {
        if ((required.name || required.surname || required.patronymic) && !(errors.name || errors.surname || errors.patronymic)) {
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
        if (required.email && required.password_for_email) {
            btn.prop({'disabled': false});
        } else {
            btn.prop({'disabled': true});
        }
    }

    function checkBtnEmailCode(btn) {
        if (required.email_code) {
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
        if (required.password_old && required.password1 && required.password2) {
            btn.prop({'disabled': false});
        } else {
            btn.prop({'disabled': true});
        }
    }

    // // Первая буква заглавная, остальные строчные
    // function formatValue(el) {
    //     let element = el[0];
    //     if (element.value !== '') {
    //         let position = element.selectionStart;
    //         element.value = element.value[0].toUpperCase() + element.value.slice(1).toLowerCase();
    //         element.selectionStart = element.selectionEnd = position;
    //     }
    // }

    function ajaxForInput(elem, btn, values) {
        let id = elem[0].id;
        if (id === 'password_old') {
            required.password_old = values.password_old.length > 0;
            // errors.password_old = !elem.val().length > 0;
            removeErrors(elem);
            checkBtnPost(btn, elem);
        } else if (id === 'password_for_email') {
            required.password_for_email = values.password_for_email.length > 0;
            // errors.password_old = !elem.val().length > 0;
            removeErrors(elem);
            checkBtnPost(btn, elem);
        } else if (id === 'email_code') {
            required.email_code = values.email_code.length > 0;
            // errors.password_old = !elem.val().length > 0;
            removeErrors(elem);
            checkBtnPost(btn, elem);
        } else {
            $.ajax({
                url: `/edit/check_input/${id}`,
                type: 'post',
                data: {
                    csrfmiddlewaretoken: csrf,
                    id: id,  // При разных url не нужен
                    values: values,
                },
                success: function (response) {
                    if (id !== 'password_old') {
                        chooseValidationColor(elem[0], response.resultStatus, response.resultError);
                    }
                    if (id === 'name') {
                        if (response.resultStatus === 'success') {
                            required.name = true;
                            errors.name = false;
                            removeErrors(elem);
                        } else if (response.resultStatus === 'error') {
                            required.name = false;
                            errors.name = response.resultError.length > 0;
                            showErrors(elem, response.resultError);
                        }
                    } else if (id === 'surname') {
                        if (response.resultStatus === 'success') {
                            required.surname = true;
                            errors.surname = false;
                            removeErrors(elem);
                        } else if (response.resultStatus === 'error') {
                            required.surname = false;
                            errors.surname = response.resultError.length > 0;
                            showErrors(elem, response.resultError);
                        }
                    } else if (id === 'patronymic') {
                        if (response.resultStatus === 'success') {
                            required.patronymic = true;
                            errors.patronymic = false;
                            removeErrors(elem);
                        } else if (response.resultStatus === 'error') {
                            required.patronymic = false;
                            errors.patronymic = response.resultError.length > 0;
                            showErrors(elem, response.resultError);
                        }
                    } else if (id === 'birthdate') {
                        if (response.resultStatus === 'success') {
                            required.birthdate = true;
                            errors.birthdate = false;
                            removeErrors(elem);
                        } else if (response.resultStatus === 'error') {
                            required.birthdate = false;
                            errors.birthdate = response.resultError.length > 0;
                            showErrors(elem, response.resultError);
                        }
                    } else if (id === 'email') {
                        if (response.resultStatus === 'success') {
                            required.email = true;
                            errors.email = false;
                            removeErrors(elem);
                        } else if (response.resultStatus === 'error') {
                            required.email = false;
                            errors.email = response.resultError.length > 0;
                            showErrors(elem, response.resultError);
                        }
                    } else if (id === 'username') {
                        if (response.resultStatus === 'success') {
                            required.username = true;
                            errors.username = false;
                            removeErrors(elem);
                        } else if (response.resultStatus === 'error') {
                            required.username = false;
                            errors.username = response.resultError.length > 0;
                            showErrors(elem, response.resultError);
                        }
                    } else if (id === 'password_old') {
                        // console.log("Старый пароль")
                        // if (response.resultStatus === 'success') {
                        //     required.password_old = true;
                        //     errors.password_old = false;
                        //     removeErrors(elem);
                        // } else if (response.resultStatus === 'error') {
                        //     required.password_old = false;
                        //     errors.password_old = true;
                        //     showErrors(elem, response.resultError);
                        // }
                    } else if (id === 'password1') {
                        // console.log(response)
                        password2.val('');
                        required.password2 = false;
                        errors.password2 = false;
                        removeErrors(password2);
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
                }
            });
        }
    }

    // Расположеие ссылки на компанию возле имени
    function positionCompany() {
        if (parseFloat(infoName.width()) + parseFloat(infoName.css('margin-left')) + parseFloat(infoName.css('margin-right')) + 30 + parseFloat(aCompany.width()) <= 680) {
            aCompany.css({
                'position': 'absolute',
                'right': '0',
                'bottom': 'calc(100% + 14px)'
            })
        } else {
            aCompany.css({
                'position': 'static',
            })
        }
        aCompany.removeClass('hide')
    }

});
