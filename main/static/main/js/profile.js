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
    }, 20000);

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
    body.on('click', '#notification-actions-menu-item', function () {
        let notification = $(this).parent().parent().parent().parent().parent();
        let category = notification.parent();
        notification.remove();
        if (category.children().length < 1) {
            category.removeClass('show')
                .addClass('hide');
            category.parent().children('.center-content-notifications-empty')
                .removeClass('hide')
                .addClass('show');
        }
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
        let data =  { selectedCategory: selectedCategory };
        $.ajax({
            url: 'loading',
            type: 'get',
            data: data,
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
                category = activeCategory;
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
});