let filterPosition = document.getElementById('filter-position');
let filterPlatform = document.getElementById('filter-platform');
let result = document.getElementById('result');
let items = result.getElementsByClassName('result');
let selectAll = document.getElementById("selectAll");

function filter() {
    for (let i = 0; i < items.length; i++) {
        if (items[i].classList.contains(filterPosition.value) && items[i].classList.contains(filterPlatform.value)) {
            items[i].style.display = '';
        } else {
            items[i].style.display = 'none';
        }
    }
    if (isFull()) {
        selectAll.checked = true;
    }
}

function resetFilter() {
    filterPosition.value = "position";
    filterPlatform.value = "platform";
    filter();
}

function selectAllOptions(el) {
    for (let i = 0; i < items.length; i++) {
        if (items[i].style.display === '') {
            items[i].getElementsByTagName("input")[0].checked = el.checked === true;
        }
    }
}

function optionCheck(el) {
    if (selectAll.checked === true && el.checked === false) {
        selectAll.checked = false;
    } else {
        if (isFull()) {
            selectAll.checked = true;
        }
    }
}

function isFull() {
    for (let i = 0; i < items.length; i++) {
        if (items[i].style.display === '' && items[i].getElementsByTagName("input")[0].checked === false) {
            return false;
        }
    }
    return true;
}