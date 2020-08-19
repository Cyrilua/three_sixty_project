$(function () {
    const body = $('body');
    const csrf = $('input[name="csrfmiddlewaretoken"]').val();


    let addPosition = $('.position__substrate');
    let menuPosition = addPosition.children('._hint-down-click').children('._hint-down-block').children('.menu');

    // Удаление отделов
    body.on('click', '#removePlatform', function () {
        let type = 'platform';
        let platform = $(this).parent().parent();
        let name = platform.attr('data-name');
        let id = platform.attr('data-id');
        let platformsBlock = platform.parent();
        // let menuPlatform = platformsBlock.children('._hint-down-click').children('._hint-down-block').children('.menu');


        console.log(platformsBlock, platformsBlock.children('.empty'))

        $.ajax({
            url: `/edit/${type}/remove/${id}`,
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
                type: type,
                id: id,
                name: name, // На всякий случай
            },
            success: function (response) {
                // if (menuPlatform.children('.menu__item').length < 1) {
                //     addPlatform.removeClass('hide');
                // }
                let newItem = document.createElement('div');
                newItem.classList.add('menu__item');
                let itemBlock = document.createElement('div');
                itemBlock.classList.add('item__block');
                $(itemBlock).attr({
                    'data-name': name,
                    'data-id': id,
                });
                itemBlock.innerText = name;
                let itemLine = document.createElement('div');
                itemLine.classList.add('item__line');
                newItem.prepend(itemLine);
                newItem.prepend(itemBlock);

                // menuPlatform.prepend(newItem);

                platform.remove();

                if (platformsBlock.children('.platform').length < 1) {
                    platformsBlock.children('.empty').removeClass('hide');
                }
            },
            error: function () {
            }
        })
    });

    // // Удаление должностей и отделов
    // body.on('click', '.remove-item', function () {
    //     let type;
    //     if ($(this).hasClass('platform__remove')) {
    //         type = 'platform';
    //     } else if ($(this).hasClass('position__remove')) {
    //         type = 'position';
    //     } else {
    //         throw new Error('Unexpected values');
    //     }
    //     let el = $(this).parent().parent();
    //     let name = el.attr('data-name');
    //     let id = el.attr('data-id');
    //
    //     $.ajax({
    //         url: `edit/${type}/remove/${id}`,
    //         type: 'post',
    //         data: {
    //             csrfmiddlewaretoken: csrf,
    //             type: type,
    //             id: id,
    //             name: name, // На всякий случай
    //         },
    //         success: function (response) {
    //             if (type === 'position' && menuPosition.children('.menu__item').length < 1) {
    //                 addPosition.removeClass('hide');
    //             } else if (type === 'platform' && menuPlatform.children('.menu__item').length < 1) {
    //                 addPlatform.removeClass('hide');
    //             }
    //             let newItem = document.createElement('div');
    //             newItem.classList.add('menu__item');
    //             let itemBlock = document.createElement('div');
    //             itemBlock.classList.add('item__block');
    //             $(itemBlock).attr({
    //                 'data-name': name,
    //                 'data-id': id,
    //             });
    //             itemBlock.innerText = name;
    //             let itemLine = document.createElement('div');
    //             itemLine.classList.add('item__line');
    //             newItem.prepend(itemLine);
    //             newItem.prepend(itemBlock);
    //             if (type === 'platform') {
    //                 menuPlatform.prepend(newItem);
    //             } else if (type === 'position') {
    //                 menuPosition.prepend(newItem);
    //             } else {
    //                 throw new Error('Unexpected values');
    //             }
    //             el.remove();
    //         },
    //         error: function () {
    //         }
    //     })
    // });

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
});