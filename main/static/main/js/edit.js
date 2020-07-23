$(function () {
    // let add = $('._hint-click');
    // let addUp = add.children('._hint-up-click');
    // let addDown = add.children('._hint-down-click');
    let body = $('body');
    let name = $('.info__name');
    let aCompany = $('.info__company');
    let openAdd;

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

    // Раскрытие/скрытие настроек
    body.on('click', '.setting__edit', function () {
        let setting = $(this.closest('.setting'));
        let settingClose = setting.children('.setting__close');
        let settingOpen = setting.children('.setting__open');
        if (settingClose.hasClass('show') && settingOpen.hasClass('hide')) {
            settingClose.removeClass('show');
            settingClose.addClass('hide');
            settingOpen.removeClass('hide');
            settingOpen.addClass('show');
        } else if (settingClose.hasClass('hide') && settingOpen.hasClass('show')) {
            settingOpen.removeClass('show');
            settingOpen.addClass('hide');
            settingClose.removeClass('hide');
            settingClose.addClass('show');
        } else {
            throw new Error('Invalid attributes');
        }
    });

    // Открыть меню (Добавить)
    body.on('click', '._hint-up-click', function () {
        let addUp = $(this.closest('._hint-click'));
        let addDown = $(addUp).children('._hint-down-click');
        addUp.toggleClass('active');
        addDown.toggle();
        openAdd = $(this).parent();
    });

    // Скрыть меню (Добавить)
    $(window).on('mouseup', function (el) {
        let _ = openAdd;
        if ($(_).children('._hint-down-click').css('display') !== 'none') {
            if (el.target.closest('._hint-up-click') !== null &&
                (el.target.closest('.position__add') !== null && ($(_).children('._hint-up-click')).hasClass('position__add')) ||
                (el.target.closest('.platform__add') !== null && ($(_).children('._hint-up-click')).hasClass('platform__add'))) {
            } else if (el.target.closest('._hint-down-click') === null || el.target.classList.contains('item__block')) {
                $(_).toggleClass('active');
                $(_).children('._hint-down-click').toggle();
            }
        }
    });

    // Добавление должностей и отделов
    body.on('click', '.item__block', function (el) {
        let typeSubstrate = el.target.closest('._hint-click');
        let type;
        if ($(typeSubstrate).hasClass('platform__substrate')) {
            type = 'platform';
        } else if ($(typeSubstrate).hasClass('position__substrate')) {
            type = 'position';
        }
        let name = $(this).text();
        let newEl = document.createElement('div');
        newEl.classList.add(type);
        let role = document.createElement('div');
        role.classList.add('role');
        role.innerText = name;
        let remove = document.createElement('div');
        remove.classList.add(`${type}__remove`);
        let cross = document.createElement('div');
        cross.classList.add('cross-in-circle');
        let circle = document.createElement('div');
        circle.classList.add('circle');
        let line1 = document.createElement('div');
        line1.classList.add('line-1');
        let line2 = document.createElement('div');
        line2.classList.add('line-2');
        newEl.prepend(role);
        role.prepend(remove);
        remove.prepend(cross);
        cross.prepend(circle);
        circle.prepend(line1);
        line1.prepend(line2);
        $(typeSubstrate).before(newEl);
    });

    // Удаление должностей
    body.on('click', '.position__remove', function () {
        let position = $(this).parent().parent();
        let positionName = position.attr('data-name');
        console.log(positionName)
        position.remove()
    });

    // Удаление отделов
    body.on('click', '.platform__remove', function () {
        let platform = $(this).parent().parent();
        let platformName = platform.attr('data-name');
        console.log(platformName)

        platform.remove()
    });
});