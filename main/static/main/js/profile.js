$(function () {
    let body = $('body');
    let moreDetails = $('.center-content-information-more-details');
    let sortable = $('.center-content-notifications-sort');
    let categories = $('.center-content-notifications-categories');

    body.on('click', '.center-content-information-more-btn', function () {
        moreDetails.toggle();
        $(this).toggleClass('active-more');
    });

    body.on('click', '.center-content-notifications-sort-category', function () {
        if (!$(this).hasClass('active-sort')) {
            sortable.children('.active-sort').removeClass('active-sort');
            $(this).addClass('active-sort');
            categories.children('.show')
                .removeClass('show')
                .addClass('hide');
            categories.children($(this).attr('data-category'))
                .removeClass('hide')
                .addClass('show');
        }
    });

    body.on('mouseenter', '._hint-up', function () {
        // console.log('hover')
        $(this).parent().children('._hint-down').css({
            'display': 'block',
        });
    });

    body.on('mouseleave', '._hint-up', function () {
        // console.log('hide')
        $(this).parent().children('._hint-down').css({
            'display': 'none',
        });
    });

    body.on('mouseenter', '._hint-up-wait', function () {
        console.log('wait hover')
        $(this).addClass('active-option');
        $(this).parent()
            .addClass('up')
            .removeClass('down');
        $(this).parent().children('._hint-down-wait').css({
            'display': 'block',
        });
    });

    body.on('mouseenter', '._hint-down-wait', function () {
        console.log('wait hover')
        $(this).parent()
            .addClass('up')
            .removeClass('down');
        $(this).css({
            'display': 'block',
        });
    });

    body.on('mouseleave', '._hint-wait', function () {
        let _ = $(this);
        _
            .addClass('down')
            .removeClass('up');
        setTimeout(function () {
            if (_.hasClass('down')) {
                console.log('wait hide')
                _.children('._hint-up-wait').removeClass('active-option');
                _.children('._hint-down-wait').css({
                    'display': 'none',
                });
            }
        }, 200)
    });

    body.on('click', '#notification-actions-menu-item', function () {
        $(this).parent().parent().parent().parent().parent().remove();
    });
});