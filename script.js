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


listObj.filter();
