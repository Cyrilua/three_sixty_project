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

    body.on('click', '.head-menu-up', function () {
        menuUp.toggleClass('active');
        menuDown.toggle();
    });

    body.on('click', '.container-fluid', function () {
        if (menuDown.css('display') !== 'none') {
            menuUp.toggleClass('active');
            menuDown.toggle();
        }
    });

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