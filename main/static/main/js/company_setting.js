$(function () {
    const body = $('body');
    const csrf = $('input[name="csrfmiddlewaretoken"]').val();
    let name = $('#companyName').val().toString();
    let description = $('#companyDescription').val().replace(/[\r\n]/g, '');

    let ajaxRemove = [];

    // Завершить все дествия перед закрытием страницы
    window.onbeforeunload = function () {
        completeRequests(ajaxRemove);
        return;
    };
    window.onunload = function () {
        return;
    };

    // Скопировать пригласительную ссылку
    body.on('click', '#copy', function (event) {
        const invite = $('#href-invite');
        invite
            .css({
                display: 'block',
            })
            .select();
        document.execCommand("copy");
        if (invite.val() !== '' && window.getSelection().toString() === invite.val()) {
            Snackbar.show({
                text: 'Ссылка скопирована',
                textColor: '#1ecb00',
                customClass: 'custom center',
                showAction: false,
                duration: 3000,
            });
        } else {
            Snackbar.show({
                text: 'Ошибка при копировании ссылки',
                textColor: '#ff0000',
                customClass: 'custom center',
                showAction: false,
                duration: 3000,
            });
        }
        invite.css({
            display: 'none',
        })

        // console.log(ajaxRemove)
    });

    // Удаление должности
    body.on('click', '#positionRemove', function (event) {
        let position = $(this).parent();
        let positionId = position.attr('data-position-id');
        let positionName = position.children('.item__text').text();
        let id;
        $.ajax({
            url: `position/${positionId}/remove/`,
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
            },
            beforeSend: function (ajax, request) {
                if (!ajaxRemove[id]) {
                    id = ajaxRemove.length;
                    ajax.abort();
                    ajaxRemove.push({
                        request: request,
                        finish: false,
                    });
                    position.addClass('hide');
                    let t = setTimeout(function () {
                        if (!ajaxRemove[id].finish) {
                            $.ajax(request);
                        }
                    }, 5000);
                    Snackbar.show({
                        text: `Должность "${positionName}" удалена`,
                        customClass: 'custom center',
                        actionText: 'Отмена',
                        actionTextColor: '#5699FF',
                        width: '910px',
                        pos: 'bottom-center',
                        duration: 5000,
                        onActionClick: function (ele) {
                            clearTimeout(t);
                            $(ele).remove();
                            ajaxRemove[id].finish = true;
                            position.removeClass('hide');
                        },
                    });
                } else {
                    position.addClass('hide');
                }
            },
            success: function (response) {
                position.remove();
                ajaxRemove[id].finish = true;
            },
            complete: function () {
            },
            error: function () {
                position.removeClass('hide');
                Snackbar.show({
                    text: `Ошибка удаления должности "${positionName}"`,
                    textColor: '#ff0000',
                    customClass: 'custom center',
                    showAction: false,
                    duration: 3000,
                });
            }
        });
    });

    // Удаление отдела
    body.on('click', '#platformRemove', function (event) {
        let platform = $(this).parent();
        let platformId = platform.attr('data-platform-id');
        let platformName = platform.children('.item__text').text();
        let id;
        $.ajax({
            url: `platform/${platformId}/remove/`,
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
            },
            beforeSend: function (ajax, request) {
                if (!ajaxRemove[id]) {
                    id = ajaxRemove.length;
                    ajax.abort();
                    ajaxRemove.push({
                        request: request,
                        finish: false,
                    });
                    platform.addClass('hide');
                    let t = setTimeout(function () {
                        if (!ajaxRemove[id].finish) {
                            $.ajax(request);
                        }
                    }, 5000);
                    Snackbar.show({
                        text: `Отдел "${platformName}" удален`,
                        customClass: 'custom center',
                        actionText: 'Отмена',
                        actionTextColor: '#5699FF',
                        width: '910px',
                        pos: 'bottom-center',
                        duration: 5000,
                        onActionClick: function (ele) {
                            clearTimeout(t);
                            $(ele).remove();
                            ajaxRemove[id].finish = true;
                            platform.removeClass('hide');
                        },
                    });
                } else {
                    platform.addClass('hide');
                }
            },
            success: function (response) {
                platform.remove();
                ajaxRemove[id].finish = true;
            },
            complete: function () {
            },
            error: function () {
                platform.removeClass('hide');
                Snackbar.show({
                    text: `Ошибка удаления отдела "${platformName}"`,
                    textColor: '#ff0000',
                    customClass: 'custom center',
                    showAction: false,
                    duration: 3000,
                });
            }
        });
    });

    // Добавление должности
    body.on('click', '#addPosition', function (event) {
        let name = $('#namePosition');
        let namePosition = name.val();
        if (namePosition.length > 0) {
            $.ajax({
                url: 'position/add/',
                type: 'post',
                data: {
                    namePosition: namePosition,
                    csrfmiddlewaretoken: csrf,
                },
                beforeSend: function (ajax) {
                    $('#positions').addClass('loading');
                },
                success: function (response) {
                    $('#positions').children('.area__body').prepend(getNewItem('position', response.positionId, namePosition));
                    name.val('');
                    $(this).prop({
                        disabled: true,
                    });
                },
                complete: function () {
                    $('#positions').removeClass('loading');
                },
                error: function () {
                    Snackbar.show({
                        text: `Произошла ошибка при добавлении должности.`,
                        textColor: '#ff0000',
                        customClass: 'custom center',
                        showAction: false,
                        duration: 3000,
                    });
                }
            });
        }
    });

    // Добавление отдела
    body.on('click', '#addPlatform', function (event) {
        let name = $('#namePlatform');
        let namePlatform = name.val();
        if (namePlatform.length > 0) {
            $.ajax({
                url: 'platform/add/',
                type: 'post',
                data: {
                    namePlatform: namePlatform,
                    csrfmiddlewaretoken: csrf,
                },
                beforeSend: function (ajax) {
                    $('#platforms').addClass('loading');
                },
                success: function (response) {
                    $('#platforms').children('.area__body').prepend(getNewItem('platform', response.platformId, namePlatform));
                    name.val('');
                    $(this).prop({
                        disabled: true,
                    });
                },
                complete: function () {
                    $('#platforms').removeClass('loading');
                },
                error: function () {
                    Snackbar.show({
                        text: 'Произошла ошибка при добавлении должности.',
                        textColor: '#ff0000',
                        customClass: 'custom center',
                        showAction: false,
                        duration: 3000,
                    });
                }
            });
        }
    });

    // Ввод названия должности
    body.on('input', '#namePosition', function (event) {
        let val = $(this).val();
        if (val.length > 0) {
            $('#addPosition').prop({
                disabled: false,
            });
        } else {
            $('#addPosition').prop({
                disabled: true,
            });
        }
    });

    // Ввод названия отдела
    body.on('input', '#namePlatform', function (event) {
        let val = $(this).val();
        if (val.length > 0) {
            $('#addPlatform').prop({
                disabled: false,
            });
        } else {
            $('#addPlatform').prop({
                disabled: true,
            });
        }
    });

    // Сохранение изменений
    body.on('click', '#saveChanges', function (event) {
        let newName = $('#companyName').val();
        let newDescription = $('#companyDescription').val();
        $.ajax({
            url: 'change/',
            type: 'post',
            data: {
                name: newName,
                description: newDescription,
                csrfmiddlewaretoken: csrf,
            },
            beforeSend: function () {
                // content.addClass('disabled');
                $('#saveChanges, #companyName, #companyDescription').prop({
                    'disabled': true,
                });
            },
            success: function () {
                name = newName;
                description = newDescription;
                $('#saveChanges').prop({
                    'disabled': true,
                });
                $('#companyName, #companyDescription').prop({
                    'disabled': false,
                });
                Snackbar.show({
                    text: 'Изменения сохранены',
                    textColor: '#07bd00',
                    customClass: 'custom center',
                    showAction: false,
                    duration: 3000,
                });
            },
            complete: function () {
                // content.removeClass('disabled');
            },
            error: function () {
                $('#saveChanges, #companyName, #companyDescription').prop({
                    'disabled': false,
                });
                Snackbar.show({
                    text: 'Произошла ошибка при сохранении.',
                    textColor: '#ff0000',
                    customClass: 'custom center',
                    showAction: false,
                    duration: 3000,
                });
            }
        });
    });

    // Можно сохранить изменения
    body.on('input keydown', '#companyName, #companyDescription', function (event) {
        if (event.keyCode === 13) {
            event.preventDefault();
        } else {
            let nameVal;
            let descriptionVal;
            if (this.id === 'companyName') {
                nameVal = $(this).val();
                descriptionVal = $('#companyDescription').val();
            } else if (this.id === 'companyDescription') {
                nameVal = $('#companyName').val();
                descriptionVal = $(this).val();
            }
            if (nameVal.length > 0 && descriptionVal.length > 0 && (descriptionVal.replace(/[\r\n]/g, '') !== description || nameVal !== name)) {
                $('#saveChanges').prop({
                    'disabled': false,
                });
                // console.log(false)
            } else {
                $('#saveChanges').prop({
                    'disabled': true,
                });
                // console.log(true)
            }
        }
    });

    // Functions

    /**
     * getNewItem
     *
     * @param {string} type
     * @param {number} id
     * @param {string} value
     * @returns {HTMLDivElement}
     */
    function getNewItem(type, id, value) {
        if (type !== 'position' && type !== 'platform') {
            throw new Error('Unexpected argument on item creation');
        }
        let item = document.createElement('div');
        $(item).addClass('area__item');
        if (type === 'position') {
            $(item).attr({
                'data-position-id': id,
            });
        } else if (type === 'platform') {
            $(item).attr({
                'data-platform-id': id,
            });
        }
        let text = document.createElement('div');
        $(text)
            .addClass('item__text')
            .text(value);
        $(item).append(text);
        let remove = document.createElement('img');
        $(remove)
            .addClass('item__remove')
            .attr({
                'src': '/static/main/images/icon/clear-24px.svg',
                'id': `${type}Remove`,
            });
        $(item).append(remove);
        return item
    }

    // При уходе со страницы завершить все действия, если они не были завершены и не были отменены
    function completeRequests(ajaxRequests) {
        for (let id = 0; id < ajaxRequests.length; id++) {
            if (!ajaxRequests[id].finish) {
                $.ajax(ajaxRequests[id].request);
            }
        }
    }
});