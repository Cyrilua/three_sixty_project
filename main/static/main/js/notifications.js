$(function () {
    $('.notification-button-cross').click(function () {
        let el = $(this)[0].parentElement.parentElement;
        el.classList.add('notification-remove');
        setTimeout(function () {
            el.remove()
        }, 500);
    });

    $('.notifications-delete-all').click(function () {
        let el = $('.notification');
        el.addClass('notification-remove');
        setTimeout(function () {
            el.remove();
        }, 500);
    })
});