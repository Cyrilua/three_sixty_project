$(function () {
    let body = $('body, html');
    body.addClass('preloader-hiding');
    setTimeout(() => (
        body.addClass('done')
    ), 200);
});
