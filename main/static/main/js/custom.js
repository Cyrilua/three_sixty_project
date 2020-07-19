function copyText(el) {
    let $tmp = $("<input>");
    $("body").append($tmp);
    $tmp.val($(el).text()).select();
    document.execCommand("copy");
    $tmp.remove();
}

function updateTextForRange(el1, el2) {
    let range = document.getElementById(el1);
    let label = document.getElementById(el2);
    label.innerText = range.value;
}

function getCounterSymbols(el1, el2) {
    let text = document.getElementById(el1);
    let counter = document.getElementById(el2);
    counter.innerText = (500 - text.value.length).toString();
}

$(function () {
    let headMenu = $('.head-menu');
    let menuUp = headMenu.children('.head-menu-up');
    let menuDown = headMenu.children('.head-menu-down');
    let body = $('body');

    // Открыть меню (в шапке)
    body.on('click', '.head-menu-up', function () {
        menuUp.toggleClass('active');
        menuDown.toggle();
    });

    // Скрыть меню при клике в любом месте (под шапкой)
    body.on('mouseup', function (el) {
        if (menuDown.css('display') !== 'none') {
            if (el.target.closest('.head-menu') === null) {
                menuUp.toggleClass('active');
                menuDown.toggle();
            }
        }
    });

    // Анимация для длинного названия компании
    body.on('mouseenter', '#head-menu-company', function () {
        let id = this.id;
        if (id === 'head-menu-company') {
            let block = $(this).children('.head-menu-item-text-block');
            let text = block.children('.head-menu-item-text');
            block.css({'overflow': 'visible'});
            let width = parseFloat(text.css('width')) * (-1) + $(this).width();
            let timeAnimation = Math.abs((width - parseFloat(text.css('margin-left'))) * 15);
            // let timeAnimationBack = Math.abs(width * 15);
            let timeAnimationBack = 0;
            block.css({'overflow': 'hidden'});
            body.on('mouseleave', '#head-menu-company', function () {
                if (text.hasClass('in')) {
                    text.removeClass('in');
                    text.addClass('out');
                    // text.stop().animate({
                    //     'margin-left': 0,
                    // }, (parseFloat(text.css('margin-left')) * -15));
                    text.stop().animate({
                        'margin-left': 0,
                    }, 0);
                }
            });
            if (text.hasClass('out')) {
                text.removeClass('out');
            }
            if (!text.hasClass('in')) {
                text.addClass('in');
                if (width < 0) {
                    text.stop().animate({
                        'margin-left': width + 'px',
                    }, timeAnimation, function () {
                        if (text.hasClass('in')) {
                            text.removeClass('in');
                            text.addClass('out');
                        }
                        text.stop().animate({
                            'margin-left': 0,
                        }, timeAnimationBack);
                    });
                }
            }
        }
    });

    // Перуходы по кнопкам в меню (в шапке)
    body.on('click', '.head-menu-item', function () {
        let id = this.id;
        if (id === 'head-menu-company') {
            $(location).attr({href: '/company_view/'});
        } else if (id === 'head-menu-settings') {
            $(location).attr({href: '/edit/'});
        } else if (id === 'head-menu-logout') {
            $(location).attr({href: '/logout/'});
        } else {
            throw new Error('invalid argument value');
        }
    });
});