$(function () {
    const body = $('body');
    const csrf = $('input[name="csrfmiddlewaretoken"]').val();
    let name = $('#companyName').val().toString();
    let description = $('#companyDescription').val().replace(/[\r\n]/g, '');

    // Удаление должности
    body.on('click', '#positionRemove', function (event) {
        
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
                        text: 'Произошла ошибка при добавлении должности.',
                        textColor: '#ff0000',
                        customClass: 'custom no-animation',
                        showAction: false,
                        duration: 3000,
                    });
                }
            });
        }
    });

    // Добавление платформы
    body.on('click', '#addPlatform', function (event) {
        let name = $('#namePlatform');
        let namePlatform = name.val();
        if (namePlatform.length > 0) {
            $.ajax({
                url: 'platform/add/',
                type: 'post',
                data: {
                    namePlatform: namePlatform,
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
                        customClass: 'custom no-animation',
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

    // Ввод названия платформы
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
            },
            beforeSend: function () {
                content.addClass('disabled');
            },
            success: function () {
                name = newName;
                description = newDescription;
                $('#saveChanges').prop({
                    'disabled': true,
                });
                Snackbar.show({
                    text: 'Сохранения сохранены.',
                    textColor: '#07bd00',
                    customClass: 'custom no-animation',
                    showAction: false,
                    duration: 3000,
                });
            },
            complete: function () {
                content.removeClass('disabled');
            },
            error: function () {
                Snackbar.show({
                    text: 'Произошла ошибка при сохранении.',
                    textColor: '#ff0000',
                    customClass: 'custom no-animation',
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
                console.log(false)
            } else {
                $('#saveChanges').prop({
                    'disabled': true,
                });
                console.log(true)
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
            });
        $(item).append(remove);
        return item
    }
});