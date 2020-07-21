$(function () {
    let body = $('body');
    // let search = $('.search__input');
    let result = $('.result');
    let resultTeams = result.children('.teams');
    let teams = resultTeams.children('.team');
    let resultEmpty = result.children('.result__empty');
    let resultNotFind = result.children('.result__not-find');

    // При загрузке
    if (teams.length < 1) {
        if (resultTeams.hasClass('show')) {
            resultTeams.removeClass('show');
            resultTeams.addClass('hide');
        }
        if (resultEmpty.hasClass('hide')) {
            resultEmpty.removeClass('hide');
            resultEmpty.addClass('show');
        }
    }

    // Поиск по названию
    body.on('input', '.search__input', function () {
        if (teams.length > 0) {
            let filter = $(this).val().toLowerCase();
            let countResult = 0;
            for (let i = 0; i < teams.length; i++) {
                let team = $(teams[i]);
                let teamName = team.attr('data-name').toLowerCase();
                if (teamName.indexOf(filter) !== -1) {
                    countResult++;
                    team.removeClass('hide');
                    team.addClass('show');
                } else {
                    team.removeClass('show');
                    team.addClass('hide');
                }
            }
            if (countResult === 0) {
                if (resultTeams.hasClass('show')) {
                    resultTeams.removeClass('show');
                    resultTeams.addClass('hide');
                }
                if (resultNotFind.hasClass('hide')) {
                    resultNotFind.removeClass('hide');
                    resultNotFind.addClass('show');
                }
            } else {
                if (resultTeams.hasClass('hide')) {
                    resultTeams.removeClass('hide');
                    resultTeams.addClass('show');
                }
                if (resultNotFind.hasClass('show')) {
                    resultNotFind.removeClass('show');
                    resultNotFind.addClass('hide');
                }
            }
        }
    });
});