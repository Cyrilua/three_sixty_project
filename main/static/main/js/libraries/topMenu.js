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
        categoriesBlock.removeClass('hidden');
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


// EXAMPLE OF USE HTML
//
//<div class="polls categories-block hidden">
//  <div class="substrate">
//      <div class="sort rounded-block unselectable">
//          <div class="category active-sort" data-category=".my-polls">
//              <div class="category__title">Мои опросы
//                  <div class="category__notice hide"></div>
//              </div>
//          </div>
//          <div class="category" data-category=".polls">
//              <div class="category__title">Для прохождения
//                  <div class="category__notice hide"></div>
//              </div>
//          </div>
//      </div>
//  </div>
//  <div class="categories">
//      <div class="category-content my-polls">
//          <div class="category-item"></div>
//          <div class="category-item"></div>
//          <div class="category-item"></div>
//      </div>
//      <div class="category-content polls">
//          <div class="category-item"></div>
//          <div class="category-item"></div>
//          <div class="category-item"></div>
//      </div>
//      <div class="category-empty center-content-notifications-empty">
//          {% include 'main/includes/bad_search.html' with text="Пока опросов нет" only %}
//      </div>
//  </div>
//</div>