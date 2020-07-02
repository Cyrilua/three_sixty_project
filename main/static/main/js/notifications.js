$(function () {
    // Удаление одного уведомления
    $('.notification-button-cross').click(function () {
        let notif = $(this)[0].parentElement.parentElement;
        let dateNotifs = notif.parentElement;
        let cleanDateNotifs = cleanChildren(Array.from(dateNotifs.children), 'notification-remove');
        if (cleanDateNotifs.length === 1) {
            let notifsDateNotifs = dateNotifs.parentElement;
            notif.classList.add('notification-remove');
            notifsDateNotifs.classList.add('notifications-date-remove');
            setTimeout(function () {
                notifsDateNotifs.remove();
            }, 500);
            let notifications = $('.notifications')[0];
            if (cleanChildren(Array.from(notifications.children), 'notifications-date-remove').length === 0) {
                setTimeout(function () {
                    notifications.remove();
                }, 500);
            }
        } else {
            notif.classList.add('notification-remove');
            setTimeout(function () {
                notif.remove();
            }, 500);
        }
    });

    // // Удаление всех уведомлений
    // $('.notifications-delete-all').click(function () {
    //     let el = $('.notifications');
    //     el.addClass('notifications-remove');
    //     setTimeout(function () {
    //         el.remove();
    //     }, 500);
    // });

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