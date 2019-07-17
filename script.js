function textParser(filterString){
  if (filterString.indexOf('>') != -1){
    filter = filterString.split('>');
    return [filter[0],'>',filter[1]];
  }
  if(filterString.indexOf('<') != -1){
    filter = filterString.split('<');
    return [filter[0],'<',filter[1]];
  }
  return filterString
}

function myFunction() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    filterProps = textParser(filter);
    ul = document.getElementById("myUL");
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName(filterProps[0].trim())[0];
        console.log(a);
        txtValue = a.textContent || a.innerText;
        if(filterProps[1] == '>'){
        	if (txtValue.toUpperCase() >= (filterProps[2].trim().toUpperCase())) {
            	li[i].style.display = "";
        	} else {
            	li[i].style.display = "none";
        	}
        }
        else if(filterProps[1] == '<'){
        	if (txtValue.toUpperCase() < (filterProps[2].trim().toUpperCase())) {
            	li[i].style.display = "";
        	} else {
            	li[i].style.display = "none";
        	}
        }
    }
}
