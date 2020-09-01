$(function () {
    const body = $('body');
    const csrf = $('input[name="csrfmiddlewaretoken"]').val();
    const content = $('.content__body');

    let ajaxRemoveTeams = [];
    let ajaxDismisses = [];
    let ajaxLoad;

    // // Новый опрос внутри компании
    // body.on('click', '#newPoll', function (event) {
    //     //TODO
    // });

    // Поиск
    body.on('input', '.search', function (event) {
        let category = $('.active-sort').attr('data-category');
        let input = $(this).val();
        loading(category, category, input);
    });

    // Смена категории
    body.on('click', '.category', function (event) {
        let active = $('.active-sort');
        let activeCategory = active.attr('data-category');
        let selectedCategory = $(this).attr('data-category');
        // console.log(activeCategory)
        if (activeCategory !== selectedCategory) {
            let search = $('.search');
            search.val('');
            let input = search.val();
            loading(activeCategory, selectedCategory, input);
        }
    });

    // Дуйствия при уходе со страницы
    window.onbeforeunload = function () {
        completeRequests(ajaxDismisses);
        completeRequests(ajaxRemoveTeams);
        return;
    };
    window.onunload = function () {
        return;
    };

    // Удаление команд
    body.on('click', '#removeTeam', function (event) {
        let team = $(this).parent();
        let teamName = team.children('.team__info').children('.team__name').children('.team__name').text();
        let teamId = team.attr('data-team-id');
        let id;
        // console.log(user, teamId)
        $.ajax({
            url: `team/${teamId}/remove/`,
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
            },
            beforeSend: function (ajax, request) {
                if (!ajaxRemoveTeams[id]) {
                    id = ajaxRemoveTeams.length;
                    ajax.abort();
                    ajaxRemoveTeams.push({
                        request: request,
                        finish: false,
                    });
                    team.addClass('hide');
                    let t = setTimeout(function () {
                        if (!ajaxRemoveTeams[id].finish) {
                            $.ajax(request);
                        }
                    }, 5000);
                    Snackbar.show({
                        text: `Команда "${teamName}" была удалена`,
                        customClass: 'custom no-animation center',
                        actionText: 'Отмена',
                        actionTextColor: '#5699FF',
                        width: '910px',
                        pos: 'bottom-center',
                        duration: 5000,
                        onActionClick: function (ele) {
                            clearTimeout(t);
                            $(ele).remove();
                            ajaxRemoveTeams[id].finish = true;
                            team.removeClass('hide');
                        },
                    });
                } else {
                }
            },
            success: function (response) {
                team.remove();
            },
            complete: function () {
                ajaxRemoveTeams[id].finish = true;
            },
            error: function () {
                team.removeClass('hide');
                Snackbar.show({
                    text: `Произошла ошибка при удалении "${teamName}"`,
                    textColor: '#ff0000',
                    customClass: 'custom no-animation',
                    showAction: false,
                    duration: 3000,
                });
            }
        })
    });

    // Удаление юзеров из компании
    body.on('click', '#dismiss', function (event) {
        let user = $(this).parent().parent().parent().parent();
        let userName = user.children('.user__view').children('.info').children('.info__top').children('.user-href').text();
        let userId = user.attr('data-real-id');
        let id;
        // console.log(user, userId)
        $.ajax({
            url: `user/${userId}/dismiss/`,
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
            },
            beforeSend: function (ajax, request) {
                if (!ajaxDismisses[id]) {
                    id = ajaxDismisses.length;
                    ajax.abort();
                    ajaxDismisses.push({
                        request: request,
                        finish: false,
                    });
                    user.addClass('hide');
                    let t = setTimeout(function () {
                        if (!ajaxDismisses[id].finish) {
                            $.ajax(request);
                        }
                    }, 5000);
                    Snackbar.show({
                        text: `${userName} был удален из компании`,
                        customClass: 'custom no-animation center',
                        actionText: 'Отмена',
                        actionTextColor: '#5699FF',
                        width: '910px',
                        pos: 'bottom-center',
                        duration: 5000,
                        onActionClick: function (ele) {
                            clearTimeout(t);
                            $(ele).remove();
                            ajaxDismisses[id].finish = true;
                            user.removeClass('hide');
                        },
                    });
                } else {
                }
            },
            success: function (response) {
                user.remove();
            },
            complete: function () {
                ajaxDismisses[id].finish = true;
            },
            error: function () {
                user.removeClass('hide');
                // $(user).css({
                //     'display': 'flex',
                // });
                Snackbar.show({
                    text: `Произошла ошибка при удалении ${userName}`,
                    textColor: '#ff0000',
                    customClass: 'custom center',
                    showAction: false,
                    duration: 3000,
                });
            }
        })
    });

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
    body.on('click', '#addPlatform', function (event) {
        let typeSubstrate = $(event.target).closest('._hint-click');
        let platformsBlock = typeSubstrate.parent();
        let namePlatform = $(this).attr('data-name');
        let idPlatform = $(this).attr('data-id');
        let menuPlatform = typeSubstrate.children('._hint-down-click').children('._hint-down-block').children('.menu');
        let user = platformsBlock.parent().parent().parent().parent();
        let pNp = user.children('.user__view').children('.info').children('.info__bottom').children('.positions-n-platforms');
        let lastPlatformView = pNp.children('.platform:last');
        let userId = user.attr('data-real-id');

        $.ajax({
            url: `user/${userId}/edit/platform/${idPlatform}/add/`,
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
                namePlatform: namePlatform, // На всякий случай
            },
            success: function (response) {
                // edit
                if (platformsBlock.children('.platform').length === 0) {
                    platformsBlock.children('.empty').addClass('hide');
                }
                $(typeSubstrate).before(getNewRoundedStrip('platform', namePlatform, idPlatform));
                $(event.target).parent().remove();
                if (menuPlatform.children('.menu__item').length < 1) {
                    $(typeSubstrate).addClass('hide');
                }

                // view
                if (lastPlatformView.length === 1) {
                    lastPlatformView.after(getNewRoundedStrip('platform', namePlatform, idPlatform, false));
                } else {
                    pNp.append(getNewRoundedStrip('platform', namePlatform, idPlatform, false));
                }
            },
            error: function () {
            }
        });
    });

    // Добавление должностей
    body.on('click', '#addPosition', function (event) {
        let typeSubstrate = $(event.target).closest('._hint-click');
        let positionsBlock = typeSubstrate.parent();
        let namePosition = $(this).attr('data-name');
        let idPosition = $(this).attr('data-id');
        let menuPosition = typeSubstrate.children('._hint-down-click').children('._hint-down-block').children('.menu');
        let user = positionsBlock.parent().parent().parent().parent();
        let pNp = user.children('.user__view').children('.info').children('.info__bottom').children('.positions-n-platforms');
        let lastPositionView = pNp.children('.position:last');
        let userId = user.attr('data-real-id');
        // console.log(lastPositionView)

        $.ajax({
            url: `user/${userId}/edit/position/${idPosition}/add/`,
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
                namePosition: namePosition, // На всякий случай
            },
            success: function (response) {
                // edit
                if (positionsBlock.children('.position').length === 0) {
                    positionsBlock.children('.empty').addClass('hide');
                }
                $(typeSubstrate).before(getNewRoundedStrip('position', namePosition, idPosition));
                $(event.target).parent().remove();
                if (menuPosition.children('.menu__item').length < 1) {
                    $(typeSubstrate).addClass('hide');
                }

                // view
                if (lastPositionView.length === 1) {
                    lastPositionView.after(getNewRoundedStrip('position', namePosition, idPosition, false));
                } else {
                    pNp.prepend(getNewRoundedStrip('position', namePosition, idPosition, false));
                }
            },
            error: function () {
            }
        });
    });

    // Добавление ролей
    body.on('click', '#addRole', function (event) {
        let typeSubstrate = $(event.target).closest('._hint-click');
        let rolesBlock = typeSubstrate.parent();
        let roleName = $(this).attr('data-role');
        let menuRoles = typeSubstrate.children('._hint-down-click').children('._hint-down-block').children('.menu');
        let user = rolesBlock.parent().parent().parent().parent().parent();
        let userInfoTop = user.children('.user__view').children('.info').children('.info__top');
        let userId = user.attr('data-real-id');

        // console.log('typeSubstrate', typeSubstrate)
        // console.log('rolesBlock', rolesBlock)
        // console.log('name', roleName)
        // console.log('menuRoles', menuRoles)

        $.ajax({
            url: `user/${userId}/edit/role/add/`,   // roleName = master | moderator
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
                roleName: roleName,
            },
            success: function (response) {
                // edit
                if (rolesBlock.children('.user__role').length === 0) {
                    rolesBlock.children('.empty').addClass('hide');
                }
                $(typeSubstrate).before(getNewRole(roleName));
                $(event.target).parent().remove();
                if (menuRoles.children('.menu__item').length < 1) {
                    $(typeSubstrate).addClass('hide');
                }

                // view
                userInfoTop.append(getNewRoleMini(roleName));
            },
            error: function () {
            }
        });
    });

    // Удаление отделов
    body.on('click', '#removePlatform', function () {
        let platform = $(this).parent().parent();
        let namePlatform = platform.attr('data-name');
        let idPlatform = platform.attr('data-id');
        let platformsBlock = platform.parent();
        let addPlatform = platformsBlock.children('.platform__substrate');
        let menuPlatform = addPlatform.children('._hint-down-click').children('._hint-down-block').children('.menu');
        let user = platformsBlock.parent().parent().parent().parent();
        let pNp = user.children('.user__view').children('.info').children('.info__bottom').children('.positions-n-platforms');
        let target = pNp.children(`.platform[data-id="${idPlatform}"]`);
        let userId = user.attr('data-real-id');
        // console.log(user, pNp, target, `.platform[data-id="${id}"]`)
        $.ajax({
            url: `user/${userId}/edit/platform/${idPlatform}/remove/`,
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
                namePlatform: namePlatform, // На всякий случай
            },
            success: function (response) {
                // edit
                if (menuPlatform.children('.menu__item').length === 0) {
                    addPlatform.removeClass('hide');
                }
                menuPlatform.prepend(getNewItem('platform', namePlatform, idPlatform));
                platform.remove();
                if (platformsBlock.children('.platform').length === 0) {
                    platformsBlock.children('.empty').removeClass('hide');
                }

                //view
                target.remove();
            },
            error: function () {
            }
        })
    });

    // Удаление должностей
    body.on('click', '#removePosition', function () {
        let position = $(this).parent().parent();
        let namePosition = position.attr('data-name');
        let idPosition = position.attr('data-id');
        let positionsBlock = position.parent();
        let addPosition = positionsBlock.children('.position__substrate');
        let menuPosition = addPosition.children('._hint-down-click').children('._hint-down-block').children('.menu');
        let user = positionsBlock.parent().parent().parent().parent();
        let pNp = user.children('.user__view').children('.info').children('.info__bottom').children('.positions-n-platforms');
        let target = pNp.children(`.position[data-id="${idPosition}"]`);
        let userId = user.attr('data-real-id');
        // console.log(user, pNp, target, `.position[data-id="${id}"]`)
        $.ajax({
            url: `user/${userId}/edit/position/${idPosition}/remove/`,
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
                namePosition: namePosition, // На всякий случай
            },
            success: function (response) {
                // edit
                if (menuPosition.children('.menu__item').length === 0) {
                    addPosition.removeClass('hide');
                }
                menuPosition.prepend(getNewItem('position', namePosition, idPosition));
                position.remove();
                if (positionsBlock.children('.position').length === 0) {
                    positionsBlock.children('.empty').removeClass('hide');
                }

                //view
                target.remove();
            },
            error: function () {
            }
        })
    });

    // Удаление ролей
    body.on('click', '#removeRole', function () {
        let userRole = $(this).parent().parent();
        let roleName = userRole.attr('data-role');
        if (roleName === 'boss') {
            Snackbar.show({
                text: 'Нельзя удалить роль босса',
                textColor: '#ff1841',
                showAction: false,
                duration: 4000,
                customClass: 'custom center',
            });
            return;
        }
        let rolesBlock = userRole.parent();
        let addRole = rolesBlock.children('.role__substrate');
        let menuRole = addRole.children('._hint-down-click').children('._hint-down-block').children('.menu');
        let user = userRole.parent().parent().parent().parent().parent().parent();
        let userViewRole = user.children('.user__view').children('.info').children('.info__top').children(`.user__role[data-role=${roleName}]`);
        let userId = user.attr('data-real-id');
        // console.log(userViewRole)
        // console.log('user__role', userRole)
        // console.log('roleName', roleName)
        // console.log('rolesBlock', rolesBlock)
        // console.log('addRole', addRole)
        // console.log('menuRole', menuRole)

        $.ajax({
            url: `user/${userId}/edit/role/remove/`,   // roleName = master | moderator
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
                roleName: roleName,
            },
            success: function (response) {
                // edit
                if (menuRole.children('.menu__item').length === 0) {
                    addRole.removeClass('hide');
                }
                menuRole.prepend(getNewItemForRole(roleName));
                userRole.remove();
                if (rolesBlock.children('.user__role').length === 0) {
                    rolesBlock.children('.empty').removeClass('hide');
                }

                //view
                userViewRole.remove();
            },
            error: function () {
            }
        });
    });

    // Редактирование юзеров
    body.on('click', '#edit', function (event) {
        let user = $(this).closest('.user');
        if (user.hasClass('user--view')) {
            let beforePos = user[0].getBoundingClientRect();
            $('.user--edit').removeClass('user--edit').addClass('user--view');
            user.removeClass('user--view').addClass('user--edit');
            let afterPos = user[0].getBoundingClientRect()
            window.scrollBy(0, -(beforePos.y - afterPos.y));
        } else if (user.hasClass('user--edit')) {
            user.removeClass('user--edit').addClass('user--view');
        }
    });

    // Первый запуск
    run();

    // Functions

    /**
     * getNewRoundedStrip
     *
     * @param {string} type
     * @param {string} name
     * @param {number, string} id
     * @param {boolean} removable
     */
    function getNewRoundedStrip(type, name, id, removable = true) {
        if (type !== 'position' && type !== 'platform') {
            throw new Error('An expected type');
        }
        let newEl = document.createElement('div');
        $(newEl).attr({
            'data-name': name,
            'data-id': id,
        });
        if (removable) {
            $(newEl).addClass(type);

        } else {
            $(newEl).addClass(`${type} _hint`);
        }
        let role = document.createElement('div');
        if (removable) {
            $(role).addClass('role');
        } else {
            $(role).addClass('role _hint-up');
        }
        role.innerText = name;
        if (removable) {
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
            role.prepend(remove);
            remove.prepend(cross);
            cross.prepend(circle);
            circle.prepend(line1);
            line1.prepend(line2);
        } else {
            let hint = document.createElement('div');
            $(hint).addClass('_hint-down');
            let hintBlock = document.createElement('div');
            $(hintBlock).addClass('_hint-down-block');
            let roleInfo = document.createElement('div');
            $(roleInfo).addClass(`${type}-information role-information`);
            let info = document.createElement('div');
            $(info).addClass(`${type}__info`);

            $(newEl).prepend(hint);
            $(hint).prepend(hintBlock);
            $(hintBlock).prepend(roleInfo);
            $(roleInfo).prepend(info);
        }
        newEl.prepend(role);
        return newEl;
    }

    /**
     * getNewItem
     *
     * @param {string} type
     * @param {string} name
     * @param {string} id
     */
    function getNewItem(type, name, id) {
        let newItem = document.createElement('div');
        newItem.classList.add('menu__item');
        let itemBlock = document.createElement('div');
        itemBlock.classList.add('item__block');
        $(itemBlock).attr({
            'data-name': name,
            'data-id': id,
            'id': `add${type[0].toUpperCase() + type.slice(1)}`,
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
        if (roleName !== 'master' && roleName !== 'moderator') {
            throw new Error('An expected type');
        }
        let userRole = document.createElement('div');
        $(userRole)
            .addClass('user__role _hint unselectable')
            .attr({
                'data-role': roleName,
            });

        let role = document.createElement('div');
        $(role).addClass(`role role-${roleName} _hint-up`);
        if (roleName === 'boss') {
            throw new Error('An unexpected role');
            // role.innerText = 'Босс';
        } else if (roleName === 'moderator') {
            role.innerText = 'Модератор';
        } else if (roleName === 'master') {
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
        $(info).addClass(`${roleName}__info`);

        $(userRole).append(hint);
        $(hint).prepend(hintBlock);
        $(hintBlock).prepend(roleInfo);
        $(roleInfo).prepend(info);

        return userRole;
    }

    /**
     * getNewRoleMini
     *
     * @param {string} roleName
     */
    function getNewRoleMini(roleName) {
        let userRole = document.createElement('div');
        $(userRole)
            .addClass('user__role _hint unselectable')
            .attr({
                'data-role': roleName,
            });

        let role = document.createElement('div');
        if (roleName === 'boss') {
            throw new Error('An unexpected role');
            // $(role).addClass('role-mini role-boss _hint-up')
        } else if (roleName === 'moderator') {
            $(role).addClass('role-mini role-moderator _hint-up')
        } else if (roleName === 'master') {
            $(role).addClass('role-mini role-master _hint-up')
        } else {
            throw new Error('An unexpected role');
        }
        $(userRole).prepend(role);

        let hint = document.createElement('div');
        $(hint).addClass('_hint-down');
        let hintBlock = document.createElement('div');
        $(hintBlock).addClass('_hint-down-block');
        let roleInfo = document.createElement('div');
        $(roleInfo).addClass('role-information');
        let info = document.createElement('div');
        if (roleName === 'boss') {
            throw new Error('An unexpected role');
            // $(info).addClass('boss__info');
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

    /**
     * getNewItem
     *
     * @param {string} role
     */
    function getNewItemForRole(role) {
        let newItem = document.createElement('div');
        newItem.classList.add('menu__item');
        let itemBlock = document.createElement('div');
        itemBlock.classList.add('item__block');
        $(itemBlock).attr({
            'data-role': role,
            'id': `addRole`,
        });
        if (role === 'boss') {
            throw new Error('An unexpected role');
            // itemBlock.innerText = 'Босс';
        } else if (role === 'moderator') {
            itemBlock.innerText = 'Модератор';
        } else if (role === 'master') {
            itemBlock.innerText = 'Мастер опросов';
        } else {
            throw new Error('An unexpected role');
        }
        let itemLine = document.createElement('div');
        itemLine.classList.add('item__line');
        newItem.prepend(itemLine);
        newItem.prepend(itemBlock);
        return newItem;
    }

    // При уходе со страницы завершить все действия, если они не были завершены и не были отменены
    function completeRequests(ajaxRequests) {
        for (let id = 0; id < ajaxRequests.length; id++) {
            if (!ajaxRequests[id].finish) {
                $.ajax(ajaxRequests[id].request);
            }
        }
    }

    // Первый запуск
    function run() {
        $('.category[data-category=teams]').trigger('click');
        // loading('teams')
    }

    /**
     * loading
     *
     * @param {string} activeCategory
     * @param {string} selectedCategory
     * @param {string} input
     */
    function loading(activeCategory, selectedCategory, input) {
        let search = $('.search');
        $.ajax({
            url: 'load/',
            type: 'get',
            data: {
                category: selectedCategory,
                search: input,
                //TODO Количество подгружаемых элементов
            },
            beforeSend: function (ajax) {
                if (ajaxLoad) {
                    ajaxLoad.abort();
                }
                ajaxLoad = ajax;
                content.addClass('loading');

                $(`.active-sort[data-category=${activeCategory}]`).removeClass('active-sort');
                $(`.category[data-category=${selectedCategory}]`).addClass('active-sort');

                if (activeCategory !== selectedCategory) {
                    search.prop({
                        disabled: true,
                    })
                }
            },
            success: function (response) {
                content
                    .empty()
                    .prepend(response.content);
                if (selectedCategory === 'teams') {
                    $('.search').attr({
                        'placeholder': 'Поиск по командам...'
                    });
                } else if (selectedCategory === 'users') {
                    $('.search').attr({
                        'placeholder': 'Поиск по участникам...'
                    });
                }

            },
            complete: function (response, status) {
                if (activeCategory !== selectedCategory) {
                    search.prop({
                        disabled: false,
                    })
                }
                content.removeClass('loading');
                if (status === 'error') {
                    Snackbar.show({
                        text: 'Произошла ошибка при загрузке данных.',
                        textColor: '#ff0000',
                        customClass: 'custom center no-animation',
                        showAction: false,
                        duration: 3000,
                    });
                }
            },
            error: function () {
                $(`.active-sort[data-category=${selectedCategory}]`).removeClass('active-sort');
                $(`.category[data-category=${activeCategory}]`).addClass('active-sort');
            }
        });
    }
});