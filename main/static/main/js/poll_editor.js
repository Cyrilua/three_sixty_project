$(function () {
    $('.poll-head-navigation-cancel').click(function (event) {
        event.preventDefault();
        if (confirm('Вы действительно хотите удалить данный опрос?')) {
            alert('Удаление данного опроса');
            close();
        }
    });

    $('textarea').on('keydown', function (e) {
        if (e.keyCode === 13)
            e.preventDefault();
    });

    $('.poll-head-name').on('input', function () {
        countLines($(this)[0], 0);
    });
    $('.poll-head-about').on('input', function () {
        countLines($(this)[0], 4);
    });
    $('.question-main-name').on('input', function () {
        countLines($(this)[0], 2);
    });
    $('.question-radio-main-answer').on('input', function () {
        countLines($(this)[0], 4);
    });

    $('.poll_questions').sortable();

    //#############################

    // $(".column").sortable({
    //     connectWith: ".column",
    //     handle: ".portlet-header",
    //     cancel: ".portlet-toggle",
    //     placeholder: "portlet-placeholder ui-corner-all"
    // });
    //
    // $(".portlet")
    //     .addClass("ui-widget ui-widget-content ui-helper-clearfix ui-corner-all")
    //     .find(".portlet-header")
    //     .addClass("ui-widget-header ui-corner-all")
    //     .prepend("<span class='ui-icon ui-icon-minusthick portlet-toggle'></span>");
    //
    // $(".portlet-toggle").on("click", function () {
    //     var icon = $(this);
    //     icon.toggleClass("ui-icon-minusthick ui-icon-plusthick");
    //     icon.closest(".portlet").find(".portlet-content").toggle();
    // });

    //#############################

    function countLines(el, delta) {
        el.style.height = '1px';
        el.style.height = (el.scrollHeight + delta) + 'px';
    }
});