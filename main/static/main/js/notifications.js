$(function () {
    // Удаление одного уведомления
    $('.notification-button-cross').click(function () {
        let el = $(this)[0].parentElement.parentElement;
        let elemsDate = el.parentElement;
        let elemsDateChildren = cleanChildren(Array.from(elemsDate.children), 'notification-remove');
        if (elemsDateChildren.length === 2) {
            el.classList.add('notification-remove');
            elemsDate.classList.add('notification-date-remove');
            setTimeout(function () {
                elemsDate.remove();
            }, 500);
            let notifications = $('.notifications')[0];
            if (cleanChildren(Array.from(notifications.children), 'notification-date-remove').length === 0) {
                setTimeout(function () {
                    notifications.remove();
                }, 500);
            }
        } else {
            el.classList.add('notification-remove');
            setTimeout(function () {
                el.remove();
            }, 500);
        }
    });

    // Удаление всех уведомлений
    $('.notifications-delete-all').click(function () {
        let el = $('.notifications');
        el.addClass('notifications-remove');
        setTimeout(function () {
            el.remove();
        }, 500);
    });

    // Очистка дочерних элемантов от ненужных
    function cleanChildren(old, cleanClass) {
        let result = [];
        old.forEach(function (e) {
            if (!e.classList.contains(cleanClass)) {
                result.push(e);
            }
        });
        return result;
    }
});