$(function () {
    let body = $('body');
    let search = $('.search__input');
    let result = $('.result');
    let resultTeams = result.children('.teams');
    let teams = resultTeams.children('.team');
    let resultEmpty = result.children('.result__empty');
    let resultNotFind = result.children('.result__not-find');

    // Поиск по названию
    body.on('input', '.search__input', function () {
        if (teams.length > 0) {
            let filter = $(this).val().toLowerCase();
            console.log(filter)
            let countResult = 0;
            for (let i = 0; i < teams.length; i++) {
                let team = $(teams[i]);
                let teamName = team.attr('data-name').toLowerCase();
                console.log(team, teamName)
                if (teamName.indexOf(filter) !== -1) {
                    console.log('show')
                    countResult++;
                    team.removeClass('hide');
                    team.addClass('show');
                } else {
                    console.log('hide')
                    team.removeClass('show');
                    team.addClass('hide');
                }
            }
            console.log(countResult)
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