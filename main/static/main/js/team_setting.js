$(function () {
    const body = $('body');
    const csrf = $('input[name="csrfmiddlewaretoken"]').val();
    const content = $('.content');
    let name = $('#teamName').val().toString();
    let description = $('#teamDescription').val().replace(/[\r\n]/g, '');
    let ajaxTeamRemove;

    // Завершить все дествия перед закрытием страницы
    window.onbeforeunload = function () {
        if (ajaxTeamRemove !== undefined) {
            $.ajax(ajaxTeamRemove);
        }
        return;
    };
    window.onunload = function () {
        return;
    };

    // Сохранение изменений
    body.on('click', '#saveChanges', function (event) {
        let newName = $('#teamName').val();
        let newDescription = $('#teamDescription').val();
        $.ajax({
            url: 'change/',
            type: 'post',
            data: {
                name: newName,
                description: newDescription,
                csrfmiddlewaretoken: csrf,
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
                    customClass: 'custom center',
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
                    customClass: 'custom center',
                    showAction: false,
                    duration: 3000,
                });
            }
        });
    });

    // Можно сохранить изменения
    body.on('input keydown', '#teamName, #teamDescription', function (event) {
        if (event.keyCode === 13) {
            event.preventDefault();
        } else {
            let nameVal;
            let descriptionVal;
            if (this.id === 'teamName') {
                nameVal = $(this).val();
                descriptionVal = $('#teamDescription').val();
            } else if (this.id === 'teamDescription') {
                nameVal = $('#teamName').val();
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
        });
    });

    // Удаление команды
    body.on('click', '#remove-team', function (event) {
        let menu = $('.menu__item ');
        $.ajax({
            url: `remove/`,
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
            },
            beforeSend: function (ajax, request) {
                if (ajaxTeamRemove === undefined) {
                    ajax.abort();
                    ajaxTeamRemove = request;
                    content.addClass('disabled');
                    menu.addClass('disabled');
                    let t = setTimeout(function () {
                        if (ajaxTeamRemove !== undefined) {
                            $.ajax(request);
                        }
                    }, 5000);
                    Snackbar.show({
                        text: 'Команда удалена',
                        customClass: 'custom center',
                        actionText: 'Отмена',
                        actionTextColor: 'yellow',
                        width: '910px',
                        duration: 5000,
                        onActionClick: function (ele) {
                            clearTimeout(t);
                            $(ele).remove();
                            content.removeClass('disabled');
                            menu.removeClass('disabled');
                            ajaxTeamRemove = undefined;
                        },
                    });
                } else {
                }
            },
            success: function (response) {
                window.onbeforeunload = function () {
                    return;
                };
                window.onunload = function () {
                    return;
                };
                location.href = '/teams/';
            },
            complete: function () {
                ajaxTeamRemove = undefined;
            },
            error: function () {
                content.removeClass('disabled');
                menu.removeClass('disabled');
                Snackbar.show({
                    text: 'Произошла ошибка при удалении команды.',
                    textColor: '#ff0000',
                    customClass: 'custom center',
                    showAction: false,
                    duration: 3000,
                });
            }
        });
    });
});