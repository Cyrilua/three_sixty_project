$(function () {
    const body = $('body');
    const csrf = $('input[name="csrfmiddlewaretoken"]').val();
    let moreDetails = $('.center-content-information-more-details');
    let name = $('.center-content-information-name');
    let aCompany = $('.center-content-information-company');
    let content = $('.body__bottom');
    let pollsNotif = $('#polls-notif');
    let resultsNotif = $('#results-notif');
    let invitesNotif = $('#invites-notif');
    let showNews = $('#showNewNotif');
    let category;
    let ajaxLoad;
    let ajaxRemoveNotif = [];

    // Дуйствия при уходе со страницы
    window.onbeforeunload = function () {
        completeRequests(ajaxRemoveNotif);
        return;
    };
    window.onunload = function () {
        return;
    };

    /**
     * При изменении размера экрана проверяем видено ли непросмотренное уведомление
     */
    $(window).resize(function () {
        checkView();
    });

    /**
     * При скролле проверяем видено ли непросмотренное уведомление
     */
    $(window).scroll(function () {
        checkView();
    });

    /**
     * Показать новые уведомления
     */
    body.on('click', '.show-new-poll', function (event) {
        $('.is_unshown').removeClass('is_unshown');
        showNews.addClass('hide');
    });

    /**
     * Проверка новых уведомлений (каждую сеекунду)
     */
    setInterval(function () {
        if (category && !content.hasClass('loading')) {
            $.ajax({
                url: 'new_notif/',
                type: 'get',
                data: {
                    category: category,
                },
                success: function (response) {
                    if (response.notificationsCount.polls > 0) {
                        pollsNotif.text(response.notificationsCount.polls);
                        pollsNotif.removeClass('hide');
                    } else {
                        pollsNotif.addClass('hide');
                    }
                    if (response.notificationsCount.results > 0) {
                        resultsNotif.text(response.notificationsCount.results);
                        resultsNotif.removeClass('hide');
                    } else {
                        resultsNotif.addClass('hide');
                    }
                    if (response.notificationsCount.invites > 0) {
                        invitesNotif.text(response.notificationsCount.invites);
                        invitesNotif.removeClass('hide');
                    } else {
                        invitesNotif.addClass('hide');
                    }

                    if (response.newElems) {
                        showNews.removeClass('hide');
                        $('.notifications').prepend(response.content);
                    }
                },
                error: function () {
                },
            });
        }
    }, 1000);

    /**
     *Просмотр уведомления на клик
     */
    body.on('click', '.notification__open', function () {
        visible($(this).parent().parent()[0], true)
    });

    /**
     * Смена категории уведомлений
     */
    body.on('click', '.category', function (event) {
        let active = $('.active-sort');
        let activeCategory = active.attr('data-category');
        let selectedCategory = $(this).attr('data-category');
        // console.log(activeCategory)
        if (activeCategory !== selectedCategory) {
            loading(activeCategory, selectedCategory);
        }
    });

    /**
     * Открыть больше информации
     */
    body.on('click', '.center-content-information-more-btn', function () {
        moreDetails.toggle();
        $(this).toggleClass('active-more');
        if ($(this).hasClass('active-more')) {
            $(this).children('.center-content-information-more-btn-text').text('Скрыть подробную информацию');
        } else {
            $(this).children('.center-content-information-more-btn-text').text('Показать подробную информацию');
        }
    });

    /**
     * Удаление уведомлений
     */
    body.on('click', '.notification__close ', function (event) {
        let notification = $(this).parent().parent();
        let notificationId = notification.attr('data-id');
        let id;
        $.ajax({
            url: `notification/${notificationId}/remove/`,
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
            },
            beforeSend: function (ajax, request) {
                if (!ajaxRemoveNotif[id]) {
                    id = ajaxRemoveNotif.length;
                    ajax.abort();
                    ajaxRemoveNotif.push({
                        request: request,
                        finish: false,
                    });
                    notification.addClass('hide');
                    let t = setTimeout(function () {
                        if (!ajaxRemoveNotif[id].finish) {
                            $.ajax(request);
                        }
                    }, 5000);
                    Snackbar.show({
                        text: `Уведомление удалено`,
                        customClass: 'custom no-animation center',
                        actionText: 'Отмена',
                        actionTextColor: '#5699FF',
                        width: '910px',
                        pos: 'bottom-center',
                        duration: 5000,
                        onActionClick: function (ele) {
                            clearTimeout(t);
                            $(ele).remove();
                            ajaxRemoveNotif[id].finish = true;
                            notification.removeClass('hide');
                        },
                    });
                } else {
                }
            },
            success: function (response) {
                notification.remove();
            },
            complete: function () {
                ajaxRemoveNotif[id].finish = true;
            },
            error: function () {
                notification.removeClass('hide');
                Snackbar.show({
                    text: `Произошла ошибка при удалении уведомления`,
                    textColor: '#ff0000',
                    customClass: 'custom center',
                    showAction: false,
                    duration: 3000,
                });
            }
        });
    });

    run();

    // Functions

    /**
     * Первый запуск
     */
    function run() {
        // Расположеие ссылки на компанию возле имени
        $(function () {
            if (parseFloat(name.width()) + parseFloat(name.css('margin-left')) + parseFloat(name.css('margin-right')) + 30 + parseFloat(aCompany.width()) <= 680) {
                aCompany.css({
                    'position': 'absolute',
                    'right': '0',
                    'bottom': 'calc(100% + 14px)'
                })
            }
            aCompany.removeClass('hide')
        });

        // Выбор категории "Для прохождения"
        $('.category[data-category=polls]').trigger('click');
    }

    /**
     * Загрузка уведомлений
     *
     * @param {string} activeCategory
     * @param {string} selectedCategory
     */
    function loading(activeCategory, selectedCategory) {
        $.ajax({
            url: 'loading',
            type: 'get',
            data: {
                selectedCategory: selectedCategory
            },
            beforeSend: function (ajax, request) {
                if (ajaxLoad) {
                    ajaxLoad.abort();
                }
                category = null;
                ajaxLoad = ajax;
                content.addClass('loading');
            },
            success: function (response) {
                $(`.active-sort[data-category=${activeCategory}]`).removeClass('active-sort');
                $(`.category[data-category=${selectedCategory}]`).addClass('active-sort');
                content.children('.notifications')
                    .empty()
                    .prepend(response.content);
                category = selectedCategory;
                // Проверка непросмотренный опросов на просмотр
                checkView();
            },
            complete: function (response, status) {
                content.removeClass('loading');
                if (status === 'error') {
                    Snackbar.show({
                        text: 'Произошла ошибка при загрузке данных.',
                        textColor: '#ff0000',
                        customClass: 'custom center',
                        showAction: false,
                        duration: 3000,
                    });
                }
            },
            error: function () {
                category = activeCategory;
            }
        })
    }

    /**
     * Просмотр нового опроса
     */
    function checkView() {
        if (!content.hasClass('loading')) {
            let noViewed = $('.no-viewed');
            // console.log(noViewed)
            for (let i = 0; i < noViewed.length; i++) {
                visible(noViewed[i], false);
            }
        }
    }

    /**
     * Проверка что элемент виден на экране или на него нажали
     * @param {HTMLElement} target
     * @param {boolean} click
     */
    function visible(target, click) {
        let targetPosition = {
            top: target.getBoundingClientRect().top + 30,
            left: target.getBoundingClientRect().left + 30,
            right: target.getBoundingClientRect().right - 30,
            bottom: target.getBoundingClientRect().bottom - 25,
        };
        let windowPosition = {
            top: 120,
            left: 0,
            right: document.documentElement.clientWidth,
            bottom: document.documentElement.clientHeight
        };
        if (!$(target).hasClass('visible-load') && (click ||
            (targetPosition.bottom < windowPosition.bottom &&
                targetPosition.top > windowPosition.top &&
                targetPosition.right < windowPosition.right &&
                targetPosition.left > windowPosition.left))) {
            let id = target.getAttribute('data-id');
            // console.log('visible')
            $.ajax({
                url: `viewing/${id}`,
                type: 'post',
                data: {
                    csrfmiddlewaretoken: csrf,
                    category: category,
                },
                beforeSend: function () {
                    $(target).addClass('visible-load');
                },
                success: function (response) {
                    $(target).removeClass('no-viewed');
                    $(target).removeClass('is_unshown');
                },
                complete: function () {
                    $(target).removeClass('visible-load');
                },
                error: function () {
                },
            })
        } else {
        }
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