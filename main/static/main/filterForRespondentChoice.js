var filter_select_el = document.getElementById('filter-position');
var items_el = document.getElementById('result');

filter_select_el.onchange = function() {
	console.log(this.value);
  var items = items_el.getElementsByClassName('position');
  for (var i=0; i<items.length; i++) {
  	if (items[i].classList.contains(this.value)) {
    	items[i].style.display = '';
    } else {
    	items[i].style.display = 'none';
    }
  }
};