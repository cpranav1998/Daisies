from dominate.tags import *
import pandas as pd
import json


def js_list(list_name: str, data: pd.DataFrame):
    """
    Python wrapper to generate a complete listjs list for displaying a pandas df.
    """
    container = div(cls="container", id=list_name)
    with container:
        br()
        search_div()
        br()
        div(input(cls="form-control", placeholder="Filter", onkeyup="myFunction()"), cls="container")
        br()
        sort_table = table(cls="table")
        with sort_table:
            make_table_header(data)
            tbody(cls="list")

    td_setup = "".join(td(cls=field).render() for field in data.columns)

    options = make_options(fields=str(list(data.columns)), table_setup=td_setup)

    records = str(data.to_dict("records"))

    js_code = """
                var options ={td_setup};
                var values ={records};
                var userList = new List('{list_name}', options, values);
                {text_parser}
                {filter};""".format(
        td_setup=options, records=str(data.to_dict("records")), list_name=list_name,
        text_parser=make_text_parser(), filter=make_filter()
    )


    return {"html": container.render(), "js": js_code}


def make_table_header(data):
    return thead().add(th(field, cls="sort", data_sort=field) for field in data.columns)


def braces_wrap(base_string):
    return "{" + base_string + "}"


def make_options(fields, table_setup):
    vals = f"valueNames: {fields},\n"
    items = f"item: '<tr>{table_setup}</tr>'"
    return braces_wrap(vals + items)

def search_div():
    return div(input(cls="search form-control", placeholder="Search"), cls="container")


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
    return """function myFunction() {
        var input, filter, ul, li, a, i, txtValue;
        input = document.getElementsByTagName("input");
        filter = input[1].value.toUpperCase();
        filterProps = textParser(filter);
        table = document.getElementsByTagName("table")[0];
        console.log(table);
        tbody = table.getElementsByTagName("tbody");
        tr = tbody[0].getElementsByTagName("tr");
        for (i = 0; i < tr.length; i++) {
            console.log(tr[i]);
            console.log(filterProps[0].trim());
            filterCategory = tr[i].getElementsByClassName(filterProps[0].trim().toLowerCase())[0];
            console.log(filterCategory);
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
                	td[i].style.display = "";
            	} else {
                	td[i].style.display = "none";
            	}
            }
        }
    };"""

