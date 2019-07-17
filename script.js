/*
function greaterThanFilter(item,filterCategory,filterValue){
  listObj.filter((item) => {
  if (item.values().${filterCategory} > filterValue) {
     return true;
  } else {
     return false;
  }
  });
}

function lessThanFilter(item,filterCategory,filterValue){
  listObj.filter((item) => {
  if (item.values().${filterCategory} < filterValue) {
     return true;
  } else {
     return false;
  }
  });
}
*/

var options = {
	valueNames: [
		'categoryOne',
		'categoryTwo',
		'categoryThree',
		{ data: ['categoryFour']}
	],
	page: 50,
	pagination: true
};
var dataList = new List('data', options);

function resetList(){
	dataList.search();
	dataList.filter();
	dataList.update();
	$(".filter-all").prop('checked', true);
	$('.filter').prop('checked', false);
	$('.search').val('');
	//console.log('Reset Successfully!');
};

function updateList(){
  var values_one = $("input[name=categoryFour]:checked").val();
	var values_two = $("input[name=categoryThree]:checked").val();
	console.log(values_one, values_two);

	dataList.filter(function (item) {
		var filterOne = false;
		var filterTwo = false;

		if(values_one == "all")
		{
			filterOne = true;
		} else {
			filterOne = item.values().categoryFour == values_one;

		}
		if(values_two == null)
		{
			filterTwo = true;
		} else {
			filterTwo = item.values().address.indexOf(values_two) >= 0;
		}
		return filterTwo && filterOne
	});
	dataList.update();
	//console.log('Filtered: ' + values_gender);
}

$(function(){
  //updateList();
  $("input[name=categoryFour]").change(updateList);
	$('input[name=categoryThree]').change(updateList);

	dataList.on('updated', function (list) {
		if (list.matchingItems.length > 0) {
			$('.no-result').hide()
		} else {
			$('.no-result').show()
		}
	});
});

/* text parser should follow standard of `category inequality_operator value` */
function textParser(filterString){
  if (filterString.find('>')){
    filter = filterString.split('>');
    return [filter[0],'>',filter[1]];
  }
  if(filterString.find('<')){
    filter = filterString.split('<');
    return [filter[0],'<',filter[1]];
  }
  return filterString
}


function filterWithoutListJs() {
  var input, filter, ul, li, a, i, txtValue;
  input = document.getElementById('inputTag');
  filterString = input.value.toUpperCase();
  filterProps = textParser(filterString);
  ul = document.getElementById("ulTag");
  li = ul.getElementsByTagName('li');

  for (i = 0; i < li.length; i++) {
    a = li[i].getElementsByTagName("elementTag")[0];
    txtValue = a.textContent || a.innerText;
    if(filterProps[1] == '>'){
      if (txtValue.toUpperCase() > filter[2]) {
        li[i].style.display = "";
      } else {
        li[i].style.display = "none";
      }
    }
    else if(filterProps[1] == '<') {
      if (txtValue.toUpperCase() < filter[2]) {
        li[i].style.display = "";
      } else {
        li[i].style.display = "none";
      }
    }
  }
}
