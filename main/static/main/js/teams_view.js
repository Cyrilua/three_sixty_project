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

    // Поиск команды
    let ajaxInput;
    body.on('input', '.head__search', function (event) {
        let search = $(this).val();
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
                content.addClass('disable');
            },
            success: function (response) {
                content.empty();
                content[0].append(response.content);
            },
            complete: function () {
                $('.content__body').removeClass('disable');
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

    // Выход из команды
    body.on('click', '.team__leave', function (event) {
        let team = $(this).parent();
        let teamId = team.attr('data-team-id');
        let id;
        $.ajax({
            url: `/team/${teamId}/remove/`,
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
                    $(team).css({
                        'display': 'none',
                    });
                    Snackbar.show({
                        text: 'Команда удалена',
                        customClass: 'custom no-animation center',
                        actionText: 'Отмена',
                        actionTextColor: 'yellow',
                        width: '910px',
                        pos: 'bottom-center',
                        duration: 5000,
                        onActionClick: function (ele) {
                            ajaxRequests[id].finish = true;
                            $(ele).remove();
                            $(team).css({
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
                $(team).remove();
            },
            complete: function () {
                ajaxRequests[id].finish = true;
            },
            error: function () {
                $(team).css({
                    'display': 'flex',
                });
                Snackbar.show({
                    text: 'Произошла ошибка при выходе вo команды.',
                    textColor: '#ff0000',
                    customClass: 'custom no-animation',
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