$(function () {
    let body = $('body');
    let templates = $('.templates');
    let currentSortable = 'date';
    let myTemplates = $('.my-templates');
    let myTemplatesBlock = $('.my-templates-block');

    let categoryContentBlock = $('.category-content');
    let countLoadedPolls = categoryContentBlock.children('.category-item');

    let scrollHeight;
    let currentScrollHeight;

    let sortable = $('.sort');

    let pollsNotif = $('#polls-notif');

    // Смена категории с уведомлениями
    body.on('click', '.category', function () {
        if (!$(this).hasClass('category-sort--active')) {
            sortable.children('.category-sort--active').removeClass('category-sort--active');
            $(this).addClass('category-sort--active');
        }
    });

    // Сортировка
    if ($('.mdc-select').length > 0) {
        const sortable = new mdc.select.MDCSelect(document.querySelector('.mdc-select'));
        sortable.listen('MDCSelect:change', () => {
            if (currentSortable !== sortable.value) {
                currentSortable = sortable.value;
                console.log(sortable.value)
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
    body.on('click', '.delete', function () {
        $(this).parent().parent().remove();
        if (myTemplates.children('.template-item').length < 1) {
            myTemplatesBlock.addClass('hide');
        }
    });

    // Проверка новых опросов (каждую сеекунду)
    setInterval(function () {
        $.ajax({
            url: 'new_notif',
            type: 'get',
            data: {},
            success: function (response) {
                if (response.notifications > 0) {
                    pollsNotif.text(response.notifications);
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
                // throw new Error('Что - то пошло не так :(');
            },
        });
    }, 1000);

    // Подгрузка данных
    $(window).scroll(function () {
        scrollHeight = Math.max(
            document.body.scrollHeight, document.documentElement.scrollHeight,
            document.body.offsetHeight, document.documentElement.offsetHeight,
            document.body.clientHeight, document.documentElement.clientHeight
        );
        currentScrollHeight = window.pageYOffset;
        if (currentScrollHeight + document.documentElement.clientHeight + 75 > scrollHeight && !categoryContentBlock.hasClass('loading')) {
            console.log(true)
            console.log('---')
            categoryContentBlock.addClass('loading');
            $.ajax({
                url: `loading/${countLoadedPolls}/`,
                type: 'get',
                data: {},
                success: function (response) {
                    categoryContentBlock.insertAdjacentHTML('beforeend', response.newElems);
                    categoryContentBlock.removeClass('loading');
                },
                statusCode: {
                    400: function () {
                        categoryContentBlock.removeClass('loading');
                        throw new Error('Error 400 - Некорректный запрос');
                    },
                    403: function () {
                        categoryContentBlock.removeClass('loading');
                        throw new Error('Error 403 - Доступ запрещён');
                    },
                    404: function () {
                        categoryContentBlock.removeClass('loading');
                        throw new Error('Error 404 - Страница не найдена');
                    },
                    500: function () {
                        categoryContentBlock.removeClass('loading');
                        throw new Error('Error 500 - Внутренняя ошибка сервера');
                    }
                },
                error: function () {
                    categoryContentBlock.removeClass('loading');
                    throw new Error('Что - то пошло не так :(');
                },
            })
        }
        // console.log(document.body.scrollHeight, document.documentElement.scrollHeight,
        //     document.body.offsetHeight, document.documentElement.offsetHeight,
        //     document.body.clientHeight, document.documentElement.clientHeight, currentScrollHeight, currentScrollHeight + document.documentElement.clientHeight)
    });
});