const maxAnswers = 5;
const maxQuestions = 5;
const timeAnimation = 200;

$(function () {
    const body = $('body');

    // $('.category-content').removeClass('hide');

    body.on('click', '.color__variable', function () {
        $('.color__variable').removeClass('color__variable--select');
        $(this).addClass('color__variable--select');
    });
});