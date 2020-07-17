$(function () {
    let body = $('body');
    let moreDetails = $('.center-content-information-more-details');
    let sortable = $('.center-content-notifications-sort');
    let categories = $('.center-content-notifications-categories');

    // Открыть больше информации
    body.on('click', '.center-content-information-more-btn', function () {
        moreDetails.toggle();
        $(this).toggleClass('active-more');
        if ($(this).hasClass('active-more')) {
            $(this).children('.center-content-information-more-btn-text').text('Скрыть подробную информацию');
        } else {
            $(this).children('.center-content-information-more-btn-text').text('Показать подробную информацию');
        }
    });

    // Смена категории с уведомлениями
    body.on('click', '.center-content-notifications-sort-category', function () {
        if (!$(this).hasClass('active-sort')) {
            sortable.children('.active-sort').removeClass('active-sort');
            $(this).addClass('active-sort');
            categories.children('.show')
                .removeClass('show')
                .addClass('hide');
            let selectedCategory = categories.children($(this).attr('data-category'));
            if (selectedCategory.children('.center-content-notification').length > 0) {
                selectedCategory
                    .removeClass('hide')
                    .addClass('show');
            } else {
                categories.children('.center-content-notifications-empty')
                    .removeClass('hide')
                    .addClass('show');
            }
        }
    });

    // Показ всплывающих окон
    body.on('mouseenter', '._hint-up', function () {
        $(this).parent().children('._hint-down').css({
            'display': 'block',
        });
    });

    // Скрытие всплывающих окон
    body.on('mouseleave', '._hint-up', function () {
        $(this).parent().children('._hint-down').css({
            'display': 'none',
        });
    });

    // Показ всплывающих окон
    body.on('mouseenter', '._hint-up-wait', function () {
        $(this).addClass('active-option');
        $(this).parent()
            .addClass('up')
            .removeClass('down');
        $(this).parent().children('._hint-down-wait').css({
            'display': 'block',
        });
    });

    // Показ всплывающих окон
    body.on('mouseenter', '._hint-down-wait', function () {
        $(this).parent()
            .addClass('up')
            .removeClass('down');
        $(this).css({
            'display': 'block',
        });
    });

    // Скрытие всплывающих окон
    body.on('mouseleave', '._hint-wait', function () {
        let _ = $(this);
        _
            .addClass('down')
            .removeClass('up');
        setTimeout(function () {
            if (_.hasClass('down')) {
                _.children('._hint-up-wait').removeClass('active-option');
                _.children('._hint-down-wait').css({
                    'display': 'none',
                });
            }
        }, 200)
    });

    // Удаление уведомлений
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
});