$(function () {
    // Скролл вверх
    $('.scroll-top-btn').click(function () {
        console.log('asd');
        $('body, html').animate({scrollTop: 0}, 400);
    });
    $(window).scroll(function () {
        let classList = $('.scroll-top-btn')[0].classList;
        if ((function () {
            return $(this).scrollTop() >= $(this).height() * 0.4
        })()) {
            if (!classList.contains('scroll-top-btn-visible')) {
                classList.add('scroll-top-btn-visible');
            }
        } else {
            if (classList.contains('scroll-top-btn-visible')) {
                classList.remove('scroll-top-btn-visible');
            }
        }
    });
});