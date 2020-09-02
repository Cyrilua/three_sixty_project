$(function () {
    const body = $('body');
    const csrf = $('input[name="csrfmiddlewaretoken"]').val();
    const content = $('.content__body');
    let ajaxRequests = [];

    window.onbeforeunload = function () {
        completeRequests();
        return;
    };
    window.onunload = function () {
        return;
    };

    // // Опрос по команде
    // body.on('click', '.new-poll', function (event) {
    //     // TODO
    // });

    // Поиск тимметов
    let ajaxInput;
    body.on('input', '.search', function (event) {
        let search = $(this).val();
        let teammates = content.children('.teammates');
        ajaxInput = $.ajax({
            url: 'search/',
            type: 'get',
            data: {
                search: search,
            },
            beforeSend: function (ajax, request) {
                if (ajaxInput) {
                    ajaxInput.abort();
                }
                content.addClass('disabled');
            },
            success: function (response) {
                teammates.empty();
                teammates.append(response.content); // ..teammates.html
            },
            complete: function () {
                $('.content__body').removeClass('disabled');
            },
            error: function () {
                // Snackbar.show({
                //     text: 'Произошла ошибка при поиске.',
                //     textColor: '#ff0000',
                //     customClass: 'custom no-animation',
                //     showAction: false,
                //     duration: 3000,
                // });
            }
        })
    });

    // Кикнуть из команды
    body.on('click', '#kick', function (event) {
        let teammate = $(this).parent();
        let teammateId = teammate.attr('data-real-id');
        let teammateName = teammate.children('.info').children('.info__top').children('.teammate-href').text();
        let id;
        $.ajax({
            url: `leave/`,
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
                teammateId: teammateId,
            },
            beforeSend: function (ajax, request) {
                if (!ajaxRequests[id]) {
                    id = ajaxRequests.length;
                    ajax.abort();
                    ajaxRequests.push({
                        request: request,
                        finish: false,
                    });
                    $(teammate).css({
                        'display': 'none',
                    });
                    Snackbar.show({
                        text: `${teammateName} был удален из команды`,
                        customClass: 'custom center',
                        actionText: 'Отмена',
                        actionTextColor: '#5699FF',
                        width: '910px',
                        duration: 5000,
                        onActionClick: function (ele) {
                            ajaxRequests[id].finish = true;
                            $(ele).remove();
                            $(teammate).css({
                                'display': 'flex',
                            });
                        },
                        onClose: function () {
                            if (!ajaxRequests[id].finish) {
                                $.ajax(request);
                            }
                        }
                    });
                } else {
                }
            },
            success: function (response) {
                teammate.remove();
            },
            complete: function () {
                ajaxRequests[id].finish = true;
            },
            error: function () {
                $(teammate).css({
                    'display': 'flex',
                });
                Snackbar.show({
                    text: 'Произошла ошибка при выходе вo команды.',
                    textColor: '#ff0000',
                    customClass: 'custom center',
                    showAction: false,
                    duration: 3000,
                });
            }
        });
    });

    // Выход из команды
    body.on('click', '#leaveTeam', function (event) {
        let teammate = $(this).parent();
        let cont = $('.content');
        let id;
        $.ajax({
            url: `leave/`,
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
            },
            beforeSend: function (ajax, request) {
                if (!ajaxRequests[id]) {
                    id = ajaxRequests.length;
                    ajax.abort();
                    ajaxRequests.push({
                        request: request,
                        finish: false,
                    });
                    cont.addClass('disabled');
                    $(teammate).css({
                        'display': 'none',
                    });
                    let t = setTimeout(function () {
                        if (!ajaxRequests[id].finish) {
                            $.ajax(request);
                        }
                    }, 5000);
                    Snackbar.show({
                        text: 'Вы покинули команду',
                        customClass: 'custom center',
                        actionText: 'Отмена',
                        actionTextColor: '#5699FF',
                        width: '910px',
                        // pos: 'bottom-center',
                        duration: 5000,
                        onActionClick: function (ele) {
                            clearTimeout(t);
                            ajaxRequests[id].finish = true;
                            $(ele).remove();
                            cont.removeClass('disabled');
                            $(teammate).css({
                                'display': 'flex',
                            });
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
                ajaxRequests[id].finish = true;
            },
            error: function () {
                cont.removeClass('disabled');
                $(teammate).css({
                    'display': 'flex',
                });
                Snackbar.show({
                    text: 'Произошла ошибка при выходе вo команды.',
                    textColor: '#ff0000',
                    customClass: 'custom center',
                    showAction: false,
                    duration: 3000,
                });
            }
        });
    });

    // При уходе со страницы завершить все удаления, если они не были завершены и не были отменены
    function completeRequests() {
        for (let id = 0; id < ajaxRequests.length; id++) {
            if (!ajaxRequests[id].finish) {
                $.ajax(ajaxRequests[id].request);
            }
        }
    }
});