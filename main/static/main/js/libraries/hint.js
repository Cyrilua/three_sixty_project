$(function () {
    let body = $('body');

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

    // Показ всплывающих окон (С ожиданием)
    body.on('mouseenter', '._hint-up-wait', function () {
        $(this).addClass('active-option');
        $(this).parent()
            .addClass('up')
            .removeClass('down');
        $(this).parent().children('._hint-down-wait').css({
            'display': 'block',
        });
    });

    // Показ всплывающих окон (С ожиданием)
    body.on('mouseenter', '._hint-down-wait', function () {
        $(this).parent()
            .addClass('up')
            .removeClass('down');
        $(this).css({
            'display': 'block',
        });
    });

    // Скрытие всплывающих окон (С ожиданием)
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
});