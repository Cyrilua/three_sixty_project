$(function () {
    const body = $('body');
    const csrf = $('input[name="csrfmiddlewaretoken"]').val();
    let templates = $('.templates');
    let currentSortable = 'date';
    let myTemplates = $('.my-templates');
    let myTemplatesBlock = $('.my-templates-block');
    const emptyBlock = $('.category-empty');

    let categoryContentBlock = $('.category-content');
    let countLoadedPolls = categoryContentBlock.children('.category-item').length;

    let sortType;
    let category = $('.category-sort--active').attr('data-category');

    let scrollHeight;
    let currentScrollHeight = 0;
    let prevScrollHeight = window.scrollY;

    window.scrollTo(0, 0);
    let sortable = $('.sort');
    let startPositionSortable = sortable[0].getBoundingClientRect().y;
    let scrollSortable = startPositionSortable;

    let pollsNotif = $('#polls-notif');

    const preloader = $('._preloader');
    const updater = $('._updater');

    const showNews = $('.show-new-poll');

    let unshowPolls = $('.unshow-polls');

    // Дуйствия при уходе со страницы
    window.onbeforeunload = function () {
        completeRequests(ajaxRemoveTemplates);
        return;
    };
    window.onunload = function () {
        return;
    };

    // Сортировка
    if ($('.mdc-select').length > 0) {
        const sortable = new mdc.select.MDCSelect(document.querySelector('.mdc-select'));
        sortType = sortable.value;
        sortable.listen('MDCSelect:change', () => {
            if (currentSortable !== sortable.value) {
                currentSortable = sortable.value;
                sortType = sortable.value;
                rerender();
            }
        });
    }

    // Первый запуск
    run();

    // Смена категории
    body.on('click', '.category', function () {
        if (!$(this).hasClass('category-sort--active')) {
            sortable.children('.category-sort--active').removeClass('category-sort--active');
            $(this).addClass('category-sort--active');
            category = $(this).attr('data-category');
            rerender();
        }
    });

    // Больше шаблонов
    body.on('click', '.more', function (el) {
        if (templates.hasClass('few')) {
            $(this).text('Скрыть');
        } else if (templates.hasClass('many')) {
            $(this).text('Больше шаблонов');
        } else {
            throw new Error('Unexpected attribute');
        }
        templates.toggleClass('few');
        templates.toggleClass('many');
    });

    // Удаление шаблонов
    let ajaxRemoveTemplates = [];
    body.on('click', '.delete', function (el) {
        let id = $(this).parent().attr('data-id');
        let template = $(el.target).parent().parent().parent().parent();
        let templateName;

        $.ajax({
            url: `template/remove/`,
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
                id: id,
            },
            beforeSend: function (ajax, request) {
                if (!ajaxRemoveTemplates[id]) {
                    id = ajaxRemoveTemplates.length;
                    ajax.abort();
                    ajaxRemoveTemplates.push({
                        request: request,
                        finish: false,
                    });
                    template.addClass('hide');
                    // if (myTemplates.children('.template-item').not('.hide').length < 1) {
                    // myTemplatesBlock.addClass('hide');
                    // $('.more')
                    //     .trigger('click')
                    // .addClass('hide');
                    // }
                    let t = setTimeout(function () {
                        if (!ajaxRemoveTemplates[id].finish) {
                            $.ajax(request);
                        }
                    }, 5000);
                    Snackbar.show({
                        text: `Шаблон "${templateName}" удален`,
                        customClass: 'custom no-animation center',
                        actionText: 'Отмена',
                        actionTextColor: 'yellow',
                        width: '910px',
                        duration: 5000,
                        onActionClick: function (ele) {
                            clearTimeout(t);
                            $(ele).remove();
                            ajaxRemoveTemplates[id].finish = true;
                            template.removeClass('hide');
                        },
                    });
                } else {
                }
            },
            success: function (response) {
                template.remove();
                // if (myTemplates.children('.template-item').not('.hide').length < 1) {
                // myTemplatesBlock.addClass('hide');
                // $('.more').remove();
                // }
            },
            complete: function () {
                ajaxRemoveTemplates[id].finish = true;
            },
            error: function () {
                template.removeClass('hide');
                // if (myTemplates.children('.template-item').not('.hide').length === 1) {
                // $('.more').trigger('click')
                // }
                Snackbar.show({
                    text: `Произошла ошибка при шаблона "${templateName}"`,
                    textColor: '#ff0000',
                    customClass: 'custom center',
                    showAction: false,
                    duration: 3000,
                });
            }
        })
    });

    // Создание нового опроса/шаблона
    body.on('click', '.template-new', function () {
        $.ajax({
            url: 'poll/create/',
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
            },
            success: function (response) {
                window.location.href = response.urlNewPoll;
            },
            error: function () {
            },
        })
    });

    // Проверка новых опросов для прохождения (каждую сеекунду)
    setInterval(function () {
        $.ajax({
            url: 'new_notif',
            type: 'get',
            data: {
                category: category,
            },
            success: function (response) {
                if (response.notifications > 0) {
                    pollsNotif.text(response.notifications);
                    pollsNotif.removeClass('hide');
                    if (response.newElems && category === 'polls') {
                        showNews.removeClass('hide');
                        emptyBlock.addClass('hide');
                        unshowPolls[0].insertAdjacentHTML('afterbegin', response.newElems);
                    }
                } else {
                    pollsNotif.addClass('hide');
                }
            },
            error: function () {
            },
        });
    }, 1000);

    // Показать новые опросы
    body.on('click', '.show-new-poll', function () {
        $(this).addClass('hide');
        let elems = unshowPolls.children('.poll-item');
        let newElems = unshowPolls.html();
        categoryContentBlock[0].insertAdjacentHTML('afterbegin', newElems);
        elems.remove();
        let newPolls = $('.new-poll');
        newPolls.removeClass('new-poll');
        // Просмотр нового опроса
        checkView();
    });


    $(window).resize(function () {
        console.log('resize')
        // Подгрузка данных при изменении размера экрана (частный случай)
        loadingPolls();
        // Просмотр нового опроса
        checkView();
    });


    $(window).scroll(function () {
        // Измерение скролла вниз
        scrollSortable = sortable[0].getBoundingClientRect().y;
        // Подгрузка данных при скролле
        loadingPolls();
        // Просмотр нового опроса
        checkView();
    });

    // Просмотр опроса на клик
    body.on('click', '.no-viewed', function () {
        visible(this, true)
    });


    // Подгрузка данных
    function loading(countNewEl, scroll) {
        if (!categoryContentBlock.hasClass('loading') && !categoryContentBlock.hasClass('full')) {
            categoryContentBlock.addClass('loading');
            sortable.addClass('disabled');
            updater.removeClass('hide');
            if (scroll) {
                preloader.removeClass('hide');
                window.scrollTo(0, 0);
                window.scrollTo(0, scroll);
            } else {
            }
            $.ajax({
                url: `loading/${countLoadedPolls}/`,
                type: 'get',
                data: {
                    count: countNewEl,
                    type: category,
                    sort: sortType,
                },
                success: function (response) {
                    if (response.newElems !== '' && response.newElems !== null) {
                        categoryContentBlock[0].insertAdjacentHTML('beforeend', response.newElems);
                        countLoadedPolls = categoryContentBlock.children('.category-item').length;
                        checkView();
                    }
                    if (response.is_last) {
                        categoryContentBlock.addClass('full');
                    } else {
                        categoryContentBlock.remove('full');
                    }
                },
                complete: function () {
                    categoryContentBlock.removeClass('loading');
                    sortable.removeClass('disabled');
                    updater.addClass('hide');
                    if (scroll) {
                        preloader.addClass('hide');
                        window.scrollTo(0, 0);
                        window.scrollTo(0, scroll);
                    } else {
                    }
                },
                error: function () {
                },
            });
        }
    }

    // Проверка что элемент виден на экране или на него нажали
    function visible(target, click) {
        let targetPosition = {
            top: target.getBoundingClientRect().top + 100,
            left: target.getBoundingClientRect().left + 30,
            right: target.getBoundingClientRect().right - 30,
            bottom: target.getBoundingClientRect().bottom - 30
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
            $.ajax({
                url: `viewing/${id}`,
                type: 'post',
                data: {
                    csrfmiddlewaretoken: csrf,
                },
                beforeSend: function () {
                    $(target).addClass('visible-load');
                },
                success: function (response) {
                    $(target).removeClass('no-viewed');
                    $(target).removeClass('new-poll');
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

    // Дейчаствия при первом запуске
    function run() {
        // Загрузка первоначальных опросов
        let heightClient = document.documentElement.clientHeight;
        let firstPartPolls = Math.ceil(heightClient / 370) * 3 + 9;
        loading(firstPartPolls);
        // Проверка непросмотренный опросов на просмотр
        checkView();
    }

    // Просмотр нового опроса
    function checkView() {
        if (category === 'polls') {
            let noViewed = $('.no-viewed');
            // console.log(noViewed)
            for (let i = 0; i < noViewed.length; i++) {
                visible(noViewed[i]);
            }
        }
    }

    // Подгрузка данных (scroll/resize)
    function loadingPolls() {
        scrollHeight = Math.max(
            document.body.scrollHeight, document.documentElement.scrollHeight,
            document.body.offsetHeight, document.documentElement.offsetHeight,
            document.body.clientHeight, document.documentElement.clientHeight
        );
        prevScrollHeight = currentScrollHeight;
        currentScrollHeight = window.pageYOffset;
        if (prevScrollHeight <= currentScrollHeight &&
            currentScrollHeight + document.documentElement.clientHeight + 150 > scrollHeight &&
            !categoryContentBlock.hasClass('loading') &&
            !categoryContentBlock.hasClass('full')) {
            let heightClient = document.documentElement.clientHeight;
            let partPolls = Math.ceil(heightClient / 370) * 3 + 9;
            loading(partPolls);
        }
    }

    // Перерисовка опросов
    function rerender() {
        categoryContentBlock.children().remove();
        countLoadedPolls = categoryContentBlock.children('.category-item').length;
        let scroll = startPositionSortable - scrollSortable;
        categoryContentBlock.removeClass('full');
        let heightClient = document.documentElement.clientHeight;
        let partPolls = Math.ceil(heightClient / 370) * 3 + 9;
        loading(partPolls, scroll);
        // checkView();
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