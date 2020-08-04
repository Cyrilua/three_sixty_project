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

    // let prevScroll = window.scrollY;
    window.scrollTo(0, 0);
    let sortable = $('.sort');
    let startPositionSortable = sortable[0].getBoundingClientRect().y;
    let scrollSortable = startPositionSortable;
    // window.scrollTo(0, prevScroll);

    let pollsNotif = $('#polls-notif');

    const preloader = $('._preloader');
    const updater = $('._updater');

    const showNews = $('.show-new-poll');

    let unshowPolls = $('.unshow-polls');

    // Первый запуск
    run();

    // Смена категории
    body.on('click', '.category', function () {
        if (!$(this).hasClass('category-sort--active')) {
            sortable.children('.category-sort--active').removeClass('category-sort--active');
            $(this).addClass('category-sort--active');
            category = $(this).attr('data-category');

            categoryContentBlock.children().remove();
            countLoadedPolls = categoryContentBlock.children('.category-item').length;
            // console.log('---')
            // console.log(countLoadedPolls)
            // console.log(sortType)
            // console.log(category)
            // console.log(scrollSortable)
            let scroll = startPositionSortable - scrollSortable;

            categoryContentBlock.removeClass('full');
            loading(9, scroll);
        }
    });

    // Сортировка
    if ($('.mdc-select').length > 0) {
        const sortable = new mdc.select.MDCSelect(document.querySelector('.mdc-select'));
        sortType = sortable.value;
        console.log(sortType)
        sortable.listen('MDCSelect:change', () => {
            if (currentSortable !== sortable.value) {
                currentSortable = sortable.value;
                console.log(sortable.value)

                // prevScrollSortable = scrollSortable;

                sortType = sortable.value;

                categoryContentBlock.children().remove();
                countLoadedPolls = categoryContentBlock.children('.category-item').length;
                // console.log('---')
                // console.log(countLoadedPolls)
                // console.log(sortType)
                // console.log(category)

                let scroll = startPositionSortable - scrollSortable;

                categoryContentBlock.removeClass('full');
                loading(9, scroll);
            }
        });
    }

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
    body.on('click', '.delete', function (el) {
        let id = $(this).parent().attr('data-id');
        $.ajax({
            url: `template/remove/`,
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
                id: id,
            },
            success: function () {
                $(el.target).parent().parent().parent().parent().remove();
                if (myTemplates.children('.template-item').length < 1) {
                    myTemplatesBlock.addClass('hide');
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
            },
        });
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
            },
        })
    });

    // body.on('click', '.poll-item', function () {
    //     $(this).removeClass('poll-item')
    //     $(this).addClass('new-poll')
    //     // $(this).remove()
    // })

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
                    console.log(response.newElems)
                    if (response.newElems && category === 'polls') {
                        showNews.removeClass('hide');
                        emptyBlock.addClass('hide');
                        unshowPolls[0].insertAdjacentHTML('afterbegin', response.newElems);
                    }
                } else {
                    pollsNotif.addClass('hide');
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
            },
        });
    }, 1000);

    // Показать новые опросы
    body.on('click', '.show-new-poll', function () {
        $(this).addClass('hide');
        let newElems = unshowPolls.children('.poll-item');
        categoryContentBlock[0].prepend(newElems);
        let newPolls = $('.new-poll');
        newPolls.removeClass('new-poll');

    });

    // Подгрузка данных при изменении размера экрана (частный случай)
    $(window).resize(function () {
        // console.log('test')

        scrollHeight = Math.max(
            document.body.scrollHeight, document.documentElement.scrollHeight,
            document.body.offsetHeight, document.documentElement.offsetHeight,
            document.body.clientHeight, document.documentElement.clientHeight
        );
        prevScrollHeight = currentScrollHeight;
        currentScrollHeight = window.pageYOffset;
        if (prevScrollHeight < currentScrollHeight &&
            currentScrollHeight + document.documentElement.clientHeight + 150 > scrollHeight &&
            !categoryContentBlock.hasClass('loading') &&
            !categoryContentBlock.hasClass('full')) {
            console.log(true)
            console.log('---')
            console.log(countLoadedPolls)
            console.log(sortType)
            console.log(category)
            loading(9);
        }
    });

    // Подгрузка данных при скролле
    $(window).scroll(function () {
        scrollHeight = Math.max(
            document.body.scrollHeight, document.documentElement.scrollHeight,
            document.body.offsetHeight, document.documentElement.offsetHeight,
            document.body.clientHeight, document.documentElement.clientHeight
        );
        prevScrollHeight = currentScrollHeight;
        currentScrollHeight = window.pageYOffset;
        if (prevScrollHeight < currentScrollHeight &&
            currentScrollHeight + document.documentElement.clientHeight + 150 > scrollHeight &&
            !categoryContentBlock.hasClass('loading') &&
            !categoryContentBlock.hasClass('full')) {
            console.log(true)
            console.log('---')
            console.log(countLoadedPolls)
            console.log(sortType)
            console.log(category)
            loading(9);
        }
        // console.log(document.body.scrollHeight, document.documentElement.scrollHeight,
        //     document.body.offsetHeight, document.documentElement.offsetHeight,
        //     document.body.clientHeight, document.documentElement.clientHeight, currentScrollHeight, currentScrollHeight + document.documentElement.clientHeight)
    });


    // Измерение скролла вниз
    $(window).scroll(function () {
        scrollSortable = sortable[0].getBoundingClientRect().y;
    });

    // Просмотр нового опроса
    $(window).scroll(function () {
        if (category === 'polls') {
            // console.log('qwe')
            let noViewed = $('.no-viewed');
            // visible(noViewed[2]);
            for (let i = 0; i < noViewed.length; i++) {
                // console.log(noViewed[i])
                visible(noViewed[i]);
            }
            console.log('----------------------------------')
        }
    });
    $(window).resize(function () {
        if (category === 'polls') {
            // console.log('qwe')
            let noViewed = $('.no-viewed');
            // visible(noViewed[2]);
            for (let i = 0; i < noViewed.length; i++) {
                // console.log(noViewed[i])
                visible(noViewed[i]);
            }
            console.log('----------------------------------')
        }
    });

    body.on('click', '.no-viewed', function () {
        visible(this, true)
    });


    // Подгрузка данных
    function loading(countNewEl, scroll) {
        if (!categoryContentBlock.hasClass('loading') && !categoryContentBlock.hasClass('full')) {
            categoryContentBlock.addClass('loading');
            sortable.addClass('disabled');
            updater.removeClass('hide');
            // preloader.removeClass('hide');
            if (scroll) {
                preloader.removeClass('hide');
                window.scrollTo(0, 0);
                window.scrollTo(0, scroll);
            } else {
                // preloader.removeClass('hidden');
                // preloader.addClass('small');
            }
            console.log(sortType)
            $.ajax({
                url: `loading/${countLoadedPolls}/`,
                type: 'get',
                data: {
                    count: countNewEl,
                    type: category,
                    sort: sortType,
                },
                success: function (response) {
                    if (response.newElems !== '') {
                        categoryContentBlock[0].insertAdjacentHTML('beforeend', response.newElems);
                        // countLoadedPolls += response.countNewElems;
                        countLoadedPolls = categoryContentBlock.children('.category-item').length;
                    }
                    console.log(response.is_last)
                    console.log(response.is_empty)
                    if (response.is_last) {
                        categoryContentBlock.addClass('full');
                    } else {
                        categoryContentBlock.remove('full');
                    }
                    if (response.is_empty) {
                        emptyBlock.removeClass('hide');
                    } else {
                        emptyBlock.addClass('hide');
                    }
                },
                complete: function () {
                    categoryContentBlock.removeClass('loading');
                    sortable.removeClass('disabled');
                    updater.addClass('hide');
                    // preloader.addClass('hide');
                    if (scroll) {
                        preloader.addClass('hide');
                        window.scrollTo(0, 0);
                        window.scrollTo(0, scroll);
                    } else {
                        // preloader.addClass('hidden');
                        // preloader.removeClass('small');
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
        // console.log(targetPosition, windowPosition)
        if (click ||
            (targetPosition.bottom < windowPosition.bottom &&
                targetPosition.top > windowPosition.top &&
                targetPosition.right < windowPosition.right &&
                targetPosition.left > windowPosition.left)) {
            // console.log('Вы видите элемент :)' );
            let id = target.getAttribute('data-id');
            // console.log(id)
            $.ajax({
                url: `viewing/${id}`,
                type: 'post',
                data: {
                    csrfmiddlewaretoken: csrf,
                },
                success: function (response) {
                    $(target).removeClass('no-viewed');
                    $(target).removeClass('new-poll');
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
                },
            })
        } else {
        }
    }

    // Дейчаствия при первом запуске
    function run() {
        // console.log('cehck')

        // Загрузка первоначальных опросов
        let heightClient = document.documentElement.clientHeight;
        let firstPartPolls = Math.ceil(heightClient / 370) + 9;
        loading(firstPartPolls);

        // Подгрузка данных, если был скролл и перезагрузка страницы (f5)
        // scrollHeight = Math.max(
        //     document.body.scrollHeight, document.documentElement.scrollHeight,
        //     document.body.offsetHeight, document.documentElement.offsetHeight,
        //     document.body.clientHeight, document.documentElement.clientHeight
        // );
        // prevScrollHeight = currentScrollHeight;
        // currentScrollHeight = window.pageYOffset;
        // console.log(prevScrollHeight < currentScrollHeight, prevScrollHeight, currentScrollHeight)
        // if (prevScrollHeight < currentScrollHeight &&
        //     currentScrollHeight + document.documentElement.clientHeight + 150 > scrollHeight &&
        //     !categoryContentBlock.hasClass('loading') &&
        //     !categoryContentBlock.hasClass('full')) {
        //     console.log(true)
        //     console.log('---')
        //     console.log(countLoadedPolls)
        //     console.log(sortType)
        //     console.log(category)
        //     loading(9);
        // }

        // Просмотр нового опроса
        if (category === 'polls') {
            // console.log('qwe')
            let noViewed = $('.no-viewed');
            // visible(noViewed[2]);
            for (let i = 0; i < noViewed.length; i++) {
                // console.log(noViewed[i])
                visible(noViewed[i]);
            }
            console.log('----------------------------------')
        }
    }
});