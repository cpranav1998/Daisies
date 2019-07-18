from dominate.tags import *
import pandas as pd
import json

def js_list(list_name: str, data: pd.DataFrame):
    """
    Python wrapper to generate a complete listjs list for displaying a pandas df.
    """
    html_div = div(cls="container", id=list_name)
    with html_div:
        br()
        div(input(cls="search form-control", placeholder="Search"), cls="container")
        br()
        div(input(cls="form-control", placeholder="Filter", onkeyup="filterFunction()"), cls="container")
        br()
        tbl = table(cls="table")
        with tbl:
            make_table_header(data)
            tbody(cls="list")

    td_setup = "".join(td(cls=field).render() for field in data.columns)

    options = """
            {{valueNames: {fields},
            item: '<tr>{table_setup}</tr>'
            }}""".format(
        fields=str(list(data.columns)), table_setup=td_setup
    )

    js_code = """
                var options ={td_setup};
                var values ={records};
                var userList = new List('{list_name}', options, values);
                {text_parser}
                {filter}
;""".format(
        td_setup=options, records=str(data.to_dict("records")), list_name=list_name,
        text_parser=make_text_parser(), filter=make_filter()
    )

    return {"html": html_div.render(), "js": js_code}


def make_table_header(data):
    return thead().add(th(field, cls="sort", data_sort=field) for field in data.columns)

def make_text_parser():
    return """function textParser(filterString){
        if (filterString.indexOf('>') != -1){
            filter = filterString.split('>');
            return [filter[0],'>',filter[1]];
        }
        if(filterString.indexOf('<') != -1){
            filter = filterString.split('<');
            return [filter[0],'<',filter[1]];
        }
        return filterString
    };"""

def make_filter():
    return """function filterFunction() {
        var input, filter, ul, li, a, i, txtValue;
        input = document.getElementsByTagName("input");
        filter = input[1].value.toUpperCase();
        filterProps = textParser(filter);
        table = document.getElementsByTagName("table")[0];
        console.log(table);
        tbody = table.getElementsByTagName("tbody");
        tr = tbody[0].getElementsByTagName("tr");
        if(filter == ''){
            for (i = 0; i < tr.length; i++){
                tr[i].style.display = "";
            }
        }
        else{
            for (i = 0; i < tr.length; i++) {
                filterCategory = tr[i].getElementsByClassName(filterProps[0].trim().toLowerCase())[0];
                txtValue = filterCategory.textContent || filterCategory.innerText;
                if(filterProps[1] == '>'){
                	if (txtValue.toUpperCase() >= (filterProps[2].trim().toUpperCase())) {
                    	tr[i].style.display = "";
                	} else {
                    	tr[i].style.display = "none";
                	}
                }
                else if(filterProps[1] == '<'){
                	if (txtValue.toUpperCase() < (filterProps[2].trim().toUpperCase())) {
                    	tr[i].style.display = "";
                	} else {
                    	tr[i].style.display = "none";
                	}
                }
            }
        }
    };"""
