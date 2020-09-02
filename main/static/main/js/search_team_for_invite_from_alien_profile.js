$(function () {
    const body = $('body');
    const csrf = $('input[name="csrfmiddlewaretoken"]').val();
    // let search = $('.search__input');
    let result = $('.result');
    let resultTeams = result.children('.teams');

    // Поиск по названию
    let ajaxSearch;
    body.on('input', '.search__input', function () {
        let search = $(this).val();
        $.ajax({
            url: 'search/',
            type: 'get',
            data: {
                search: search,
            },
            beforeSend: function (ajax) {
                if (ajaxSearch) {
                    ajaxSearch.abort();
                }
                ajaxSearch = ajax;
                $('.result').addClass('loading');
            },
            success: function (response) {
                $('.teams')
                    .empty()
                    .prepend(response.content);
            },
            complete: function () {
                $('.result').removeClass('loading');
                ajaxSearch = null;
            },
            error: function () {
                Snackbar.show({
                    text: 'Ошибка при поиске',
                    textColor: '#ff1841',
                    showAction: false,
                    duration: 3000,
                    customClass: 'custom center',
                });
            }
        })
        // if (teams.length > 0) {
        //     let filter = $(this).val().toLowerCase();
        //     let countResult = 0;
        //     for (let i = 0; i < teams.length; i++) {
        //         let team = $(teams[i]);
        //         let teamName = team.attr('data-name').toLowerCase();
        //         if (teamName.indexOf(filter) !== -1) {
        //             countResult++;
        //             team.removeClass('hide');
        //             team.addClass('show');
        //         } else {
        //             team.removeClass('show');
        //             team.addClass('hide');
        //         }
        //     }
        //     if (countResult === 0) {
        //         if (resultTeams.hasClass('show')) {
        //             resultTeams.removeClass('show');
        //             resultTeams.addClass('hide');
        //         }
        //         if (resultNotFind.hasClass('hide')) {
        //             resultNotFind.removeClass('hide');
        //             resultNotFind.addClass('show');
        //         }
        //     } else {
        //         if (resultTeams.hasClass('hide')) {
        //             resultTeams.removeClass('hide');
        //             resultTeams.addClass('show');
        //         }
        //         if (resultNotFind.hasClass('show')) {
        //             resultNotFind.removeClass('show');
        //             resultNotFind.addClass('hide');
        //         }
        //     }
        // }
    });

    // Отправка приглашения
    body.on('click', '.team__button', function (event) {
        let teamId = $(this).closest('.team').attr('data-team-id');
        $.ajax({
            url: 'send/',
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
                teamId: teamId,
            },
            beforeSend: function () {
                $(event.target).prop({
                    'disabled': true,
                });
            },
            success: function (response) {
                Snackbar.show({
                    text: 'Приглашение отправлено',
                    textColor: '#1ecb00',
                    customClass: 'custom center',
                    showAction: false,
                    duration: 3000,
                });
            },
            error: function () {
                $(event.target).prop({
                    'disabled': false,
                });
            }
        })
    });
});