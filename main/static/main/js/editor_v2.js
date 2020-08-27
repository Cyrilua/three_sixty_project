$(function () {
    const maxAnswers = 15;
    const maxQuestions = 50;
    const maxLengthInput = 150;
    const timeAnimation = 200;

    const body = $('body');
    const editor = $('.editor ');
    const menu = $('.menu-r').children('.menu').children('.menu__item');
    const csrf = $('input[name="csrfmiddlewaretoken"]').val();

    let listKeys = [];

    let pollId;
    let templateId;

    let selectedInterviewed;
    let selectedTarget = false;

    // Functions

});