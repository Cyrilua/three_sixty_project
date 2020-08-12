$(function () {
    let mySwiper = new Swiper('.swiper-container', {
        speed: 300,
        spaceBetween: 25,
        // loop: true,
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        pagination: {
            el: '.swiper-pagination',
            type: 'bullets',
        },
        autoplay: {
            delay: 3000,
        }
    });
});