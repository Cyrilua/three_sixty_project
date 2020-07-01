$(function () {
    const csrf = $('input[name="csrfmiddlewaretoken"]').val();
    let div = $('.new-poll')[0];
    $('#test').click(function () {
        $.ajax({
            url: '',
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
            },
            success: function (response) {
                div.innerHTML = response.newHTML;
                console.log(response.newHTML);
            }
        })
    })

    // const csrf = $('input[name="csrfmiddlewaretoken"]').val();
    // const search = $('#search');
    // const listItems = $('.new-poll-selection-list').children()
    // const listItemValues = listItems.children('.new-poll-selection-list-item-name').children('.new-poll-selection-list-item-checkbox');
    // const btnNext = $('.new-poll-to-step-2')[0];
    //
    // // Переход к следующему этапу
    // btnNext.click(function () {
    //     $.ajax({
    //         url: '',
    //         type: 'post',
    //         data: {
    //             //TODO
    //             csrfmiddlewaretoken: csrf,
    //         },
    //         success: function (response) {
    //             //TODO
    //         }
    //     });
    // });
    //
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
});
