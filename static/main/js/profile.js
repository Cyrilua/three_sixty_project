$(function () {
    let body = $('body');
    let moreDetails = $('.center-content-information-more-details');
    let name = $('.center-content-information-name');
    let aCompany = $('.center-content-information-company');

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

    // // Проверка на отсутствие уведомлений в первой категории сортироаки
    // $(function () {
    //     let polls = $('.center-content-notifications-polls');
    //     if (polls.children().length > 0) {
    //         polls
    //             .removeClass('hide')
    //             .addClass('show');
    //     } else {
    //         categoryEmpty
    //             .removeClass('hide')
    //             .addClass('show');
    //     }
    // });

    // // Сортировка поднимается над контентом
    // $(window).scroll(function () {
    //     let up = categorySubstrate[0].getBoundingClientRect();
    //     let down = categories[0].getBoundingClientRect();
    //     if (up.bottom >= down.top) {
    //         categorySubstrate.addClass('shadow-category');
    //     } else {
    //         categorySubstrate.removeClass('shadow-category');
    //     }
    // });

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