$(function () {
    const body = $('body');
    const csrf = $('input[name="csrfmiddlewaretoken"]').val();
    const content = $('.content__body');

    // Оправить приглашение
    body.on('click', '.invite', function (event) {
        let userId = $(this).parent().attr('data-real-id');
        $.ajax({
            url: `invite/${userId}`,
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
            },
            beforeSend: function () {
                $(event.target).prop({
                    disabled: true,
                })
            },
            success: function (){
            },
            complete: function () {
            },
            error: function () {
                $(event.target).prop({
                    disabled: false,
                });
                Snackbar.show({
                    text: 'Произошла ошибка при отправке приглашения',
                    textColor: '#ff0000',
                    customClass: 'custom center',
                    showAction: false,
                    duration: 3000,
                });
            }
        })
    });

    // Поиск
    let ajaxSearch;
    body.on('input', '#search', function (event) {
        let search = $(this).val();
        ajaxSearch = $.ajax({
            url: 'search/',
            type: 'get',
            data: {
                search: search,
            },
            beforeSend: function (ajax, request) {
                if (ajaxSearch) {
                    ajaxSearch.abort();
                }
                content.addClass('disabled');
            },
            success: function (response) {
                content.children('.users')
                    .empty()
                    .append(response.content); // ..teammates.html
            },
            complete: function () {
                $('.content__body').removeClass('disabled');
            },
            error: function () {
                // Snackbar.show({
                //     text: 'Произошла ошибка при поиске.',
                //     textColor: '#ff0000',
                //     customClass: 'custom no-animation',
                //     showAction: false,
                //     duration: 3000,
                // });
            }
        });
    });
});