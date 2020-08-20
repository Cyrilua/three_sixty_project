$(function () {
    const body = $('body');
    const csrf = $('input[name="csrfmiddlewaretoken"]').val();


    // let addPosition = $('.position__substrate');
    // let menuPosition = addPosition.children('._hint-down-click').children('._hint-down-block').children('.menu');

    let openAdd;
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
                (el.target.closest('.platform__add') !== null && ($(_).children('._hint-up-click')).hasClass('platform__add')) ||
                (el.target.closest('.role__add') !== null && ($(_).children('._hint-up-click')).hasClass('role__add'))) {
            } else if (el.target.closest('._hint-down-click') === null || el.target.classList.contains('item__block')) {
                $(_).toggleClass('active');
                $(_).children('._hint-down-click').toggle();
            }
        }
    });

    // Добавление отделов
    body.on('click', '#addPlatform', function (el) {
        let typeSubstrate = $(el.target).closest('._hint-click');
        let platformsBlock = typeSubstrate.parent();
        let name = $(this).attr('data-name');
        let id = $(this).attr('data-id');
        let menuPlatform = typeSubstrate.children('._hint-down-click').children('._hint-down-block').children('.menu');

        $.ajax({
            url: `/edit/platform/add/${id}`,
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
                type: 'platform',
                id: id,
                name: name, // На всякий случай
            },
            success: function (response) {
                if (platformsBlock.children('.platform').length === 0) {
                    platformsBlock.children('.empty').addClass('hide');
                }
                $(typeSubstrate).before(getNewRoundedStrip('platform', name, id));
                $(el.target).parent().remove();
                if (menuPlatform.children('.menu__item').length < 1) {
                    $(typeSubstrate).addClass('hide');
                }
            },
            error: function () {
            }
        });
    });

    // Добавление должностей
    body.on('click', '#addPosition', function (el) {
        let typeSubstrate = $(el.target).closest('._hint-click');
        let positionsBlock = typeSubstrate.parent();
        let name = $(this).attr('data-name');
        let id = $(this).attr('data-id');
        let menuPosition = typeSubstrate.children('._hint-down-click').children('._hint-down-block').children('.menu');

        $.ajax({
            url: `/edit/position/add/${id}`,
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
                type: 'position',
                id: id,
                name: name, // На всякий случай
            },
            success: function (response) {
                if (positionsBlock.children('.position').length === 0) {
                    positionsBlock.children('.empty').addClass('hide');
                }
                $(typeSubstrate).before(getNewRoundedStrip('position', name, id));
                $(el.target).parent().remove();
                if (menuPosition.children('.menu__item').length < 1) {
                    $(typeSubstrate).addClass('hide');
                }
            },
            error: function () {
            }
        });
    });

    // Добавление ролей
    body.on('click', '#addRole', function (el) {
        let typeSubstrate = $(el.target).closest('._hint-click');
        let rolesBlock = typeSubstrate.parent();
        let roleName = $(this).attr('data-name');
        let menuRoles = typeSubstrate.children('._hint-down-click').children('._hint-down-block').children('.menu');
        console.log('typeSubstrate', typeSubstrate)
        console.log('rolesBlock', rolesBlock)
        console.log('name', roleName)
        // console.log('id', id)
        console.log('menuRoles', menuRoles)

        if (rolesBlock.children('.position').length === 0) {
            rolesBlock.children('.empty').addClass('hide');
        }
        $(typeSubstrate).before(getNewRole(roleName));
        $(el.target).parent().remove();
        if (menuRoles.children('.menu__item').length < 1) {
            $(typeSubstrate).addClass('hide');
        }

        // $.ajax({
        //     url: `/edit/position/add/${id}`,
        //     type: 'post',
        //     data: {
        //         csrfmiddlewaretoken: csrf,
        //         type: 'position',
        //         // id: id,
        //         name: name, // На всякий случай
        //     },
        //     success: function (response) {
        //         if (rolesBlock.children('.position').length === 0) {
        //             rolesBlock.children('.empty').addClass('hide');
        //         }
        //         $(typeSubstrate).before(getNewRoundedStrip('position', name));
        //         $(el.target).parent().remove();
        //         if (menuRoles.children('.menu__item').length < 1) {
        //             $(typeSubstrate).addClass('hide');
        //         }
        //     },
        //     error: function () {
        //     }
        // });
    });

    // Удаление отделов
    body.on('click', '#removePlatform', function () {
        let platform = $(this).parent().parent();
        let name = platform.attr('data-name');
        let id = platform.attr('data-id');
        let platformsBlock = platform.parent();
        let addPlatform = platformsBlock.children('.platform__substrate');
        let menuPlatform = addPlatform.children('._hint-down-click').children('._hint-down-block').children('.menu');
        // console.log(platformsBlock, menuPlatform)
        $.ajax({
            url: `/edit/platform/remove/${id}`,
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
                type: 'platform',
                id: id,
                name: name, // На всякий случай
            },
            success: function (response) {
                if (menuPlatform.children('.menu__item').length === 0) {
                    addPlatform.removeClass('hide');
                }
                menuPlatform.prepend(getNewItem(name, id));
                platform.remove();
                if (platformsBlock.children('.platform').length === 0) {
                    platformsBlock.children('.empty').removeClass('hide');
                }
            },
            error: function () {
            }
        })
    });

    // Удаление должностей
    body.on('click', '#removePosition', function () {
        let position = $(this).parent().parent();
        let name = position.attr('data-name');
        let id = position.attr('data-id');
        let positionsBlock = position.parent();
        let addPosition = positionsBlock.children('.position__substrate');
        let menuPosition = addPosition.children('._hint-down-click').children('._hint-down-block').children('.menu');
        $.ajax({
            url: `/edit/position/remove/${id}`,
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
                type: 'position',
                id: id,
                name: name, // На всякий случай
            },
            success: function (response) {
                if (menuPosition.children('.menu__item').length === 0) {
                    addPosition.removeClass('hide');
                }
                menuPosition.prepend(getNewItem(name, id));
                position.remove();
                if (positionsBlock.children('.position').length === 0) {
                    positionsBlock.children('.empty').removeClass('hide');
                }
            },
            error: function () {
            }
        })
    });

    // Редактирование юзеров
    body.on('click', '#edit', function (event) {
        let user = $(this).closest('.user');
        if (user.hasClass('user--view')) {
            let beforePos = user[0].getBoundingClientRect()
            $('.user--edit').removeClass('user--edit').addClass('user--view');
            user.removeClass('user--view').addClass('user--edit');
            let afterPos = user[0].getBoundingClientRect()
            window.scrollBy(0, -(beforePos.y - afterPos.y));
        } else if (user.hasClass('user--edit')) {
            user.removeClass('user--edit').addClass('user--view');
        }
    });

    // Functions

    /**
     * getNewRoundedStrip
     *
     * @param {string} type
     * @param {string} name
     * @param {string} id
     */
    function getNewRoundedStrip(type, name, id) {
        let newEl = document.createElement('div');
        newEl.classList.add(type);
        $(newEl).attr({
            'data-name': name,
            'data-id': id,
        });
        let role = document.createElement('div');
        role.classList.add('role');
        role.innerText = name;
        let remove = document.createElement('div');
        let removeClassList = remove.classList;
        removeClassList.add(`${type}__remove`);
        removeClassList.add('remove-item');
        $(remove).attr({
            'id': `remove${type[0].toUpperCase() + type.slice(1)}`,
        });
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
        return newEl;
    }

    /**
     * getNewItem
     *
     * @param {string} name
     * @param {string} id
     */
    function getNewItem(name, id) {
        let newItem = document.createElement('div');
        newItem.classList.add('menu__item');
        let itemBlock = document.createElement('div');
        itemBlock.classList.add('item__block');
        $(itemBlock).attr({
            'data-name': name,
            'data-id': id,
            'id': 'addPlatform',
        });
        itemBlock.innerText = name;
        let itemLine = document.createElement('div');
        itemLine.classList.add('item__line');
        newItem.prepend(itemLine);
        newItem.prepend(itemBlock);
        return newItem;
    }

    /**
     * getNewRole
     *
     * @param {string} roleName
     */
    function getNewRole(roleName) {
        let userRole = document.createElement('div');
        $(userRole).addClass('user__role _hint unselectable');

        let role = document.createElement('div');
        if (roleName === 'boss') {
            $(role).addClass('role role-boss _hint-up');
            role.innerText = 'Босс';
        } else if (roleName === 'moderator') {
            $(role).addClass('role role-moderator _hint-up');
            role.innerText = 'Модератор';
        } else if (roleName === 'master') {
            $(role).addClass('role role-master _hint-up');
            role.innerText = 'Мастер опросов';
        } else {
            throw new Error('An unexpected role');
        }
        $(userRole).prepend(role);

        let remove = document.createElement('div');
        $(remove)
            .addClass('role__remove remove-item')
            .attr({
                'id': 'removeRole',
            });
        $(role).prepend(remove);

        let cross = document.createElement('div');
        cross.classList.add('cross-in-circle');
        let circle = document.createElement('div');
        circle.classList.add('circle');
        let line1 = document.createElement('div');
        line1.classList.add('line-1');
        let line2 = document.createElement('div');
        line2.classList.add('line-2');
        remove.prepend(cross);
        cross.prepend(circle);
        circle.prepend(line1);
        line1.prepend(line2);

        let hint = document.createElement('div');
        $(hint).addClass('_hint-down');
        let hintBlock = document.createElement('div');
        $(hintBlock).addClass('_hint-down-block');
        let roleInfo = document.createElement('div');
        $(roleInfo).addClass('role-information');
        let info = document.createElement('div');
        if (roleName === 'boss') {
            $(info).addClass('boss__info');
        } else if (roleName === 'moderator') {
            $(info).addClass('moderator__info');
        } else if (roleName === 'master') {
            $(info).addClass('master__info');
        } else {
            throw new Error('An unexpected role');
        }

        $(userRole).append(hint);
        $(hint).prepend(hintBlock);
        $(hintBlock).prepend(roleInfo);
        $(roleInfo).prepend(info);

        return userRole;
    }
});