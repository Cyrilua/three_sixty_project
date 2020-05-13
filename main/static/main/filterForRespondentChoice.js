let filterPosition = document.getElementById('filter-position');
let filterPlatform = document.getElementById('filter-platform');
let result = document.getElementById('result');

function filter() {
    // console.log(this.value);
    let items = result.getElementsByClassName('result');
    for (let i = 0; i < items.length; i++) {
        if (items[i].classList.contains(filterPosition.value) && items[i].classList.contains(filterPlatform.value)) {
            items[i].style.display = '';
        } else {
            items[i].style.display = 'none';
        }
    }
}

function resetFilter() {
    filterPosition.value = "position";
    filterPlatform.value = "platform";
    filter();
}
