$(function () {



    // const csrf = $('input[name="csrfmiddlewaretoken"]').val();
    // window.history.pushState({
    //     "pageContainer": container[0].outerHTML,
    //     'rightMenu': rightMenu[0].outerHTML,
    //     "pageTitle": history.
    // }, "Опросы", '/poll/');
    // const search = $('#search');
    // const listItems = $('.new-poll-selection-list').children()
    // const listItemValues = listItems.children('.new-poll-selection-list-item-name').children('.new-poll-selection-list-item-checkbox');
    // const btnNext = $('.new-poll-to-step-2')[0];


    // // Поиск
    // search.on('input', function () {
    //     console.log();
    //     findSubstring(search.val().toLowerCase())
    // });
    //
    // function findSubstring(substr) {
    //     for (let i = 0; i < listItemValues.length; i++) {
    //         listItems[i].hidden = (listItemValues[i].value.toLowerCase()).indexOf(substr) === -1;
    //     }
    // }

    // ################################################################################

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            let cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});