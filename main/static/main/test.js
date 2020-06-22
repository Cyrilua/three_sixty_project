$(function () {

    const token = $('input[name=csrfmiddlewaretoken]').val();

    $('.my-btn').click(function () {
        $.ajax({
            url: '',
            type: 'get',
            data: {
                button_text: $(this).text(),
            },
            success: function (response) {
                $('.result-1').text(response.result_1);
            },
        });
    });

    $('.result-1').click(function () {
       $.ajax({
           url: '',
           type: 'post',
           data: {
               text: $(this).text(),
               csrfmiddlewaretoken: token,
           },
           success: function (response) {
               $('.result-2').append(response.data_result + '<br>');
           },
       });
    });
});