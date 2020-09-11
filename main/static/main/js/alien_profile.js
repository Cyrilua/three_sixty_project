$(function () {
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
        aCompany.removeClass('hide');
    });
});