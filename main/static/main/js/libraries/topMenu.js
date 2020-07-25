$(function () {
    let body = $('body');
    let sortable = $('.sort');
    let categories = $('.categories');
    let categoryEmpty = categories.children('.category-empty');
    let categoryContent = $('.category-content');
    let categoriesBlock = $('.categories-block');

    // Скрытие ненужных элементов сразу после загрузки
    $(function () {
        categoryEmpty.addClass('hide');
        categoryContent.addClass('hide');
        if (categoryContent.first().children('.category-item').length > 0) {
            categoryContent.first().removeClass('hide').addClass('show');
        } else {
            categoryEmpty.removeClass('hide').addClass('show');
        }
        categoriesBlock.removeClass('hide');
    });

    // Смена категории с уведомлениями
    body.on('click', '.category', function () {
        if (!$(this).hasClass('active-sort')) {
            sortable.children('.active-sort').removeClass('active-sort');
            $(this).addClass('active-sort');
            categories.children('.show')
                .removeClass('show')
                .addClass('hide');
            let selectedCategory = categories.children($(this).attr('data-category'));
            if (selectedCategory.children('.category-item').length > 0) {
                selectedCategory
                    .removeClass('hide')
                    .addClass('show');
            } else {
                categoryEmpty
                    .removeClass('hide')
                    .addClass('show');
            }
        }
    });
});