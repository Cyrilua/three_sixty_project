$(function () {
    let body = $('body');
    let moreDetails = $('.center-content-information-more-details');

    body.on('click', '.center-content-information-more-btn', function () {
        moreDetails.toggle();
        $(this).toggleClass('active-more');
    });
});