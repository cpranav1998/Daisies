from dominate.tags import *
import pandas as pd
import json
import os

class CSS:
    def __init__(self, name: str):
        print(os.getcwd())
        with open("./lists/css/{filename}.json".format(filename=name)) as json_file:
            stylesDict = json.load(json_file)
            self.styles = stylesDict["style"]
            self.fonts = stylesDict["fonts"]
    def __apply_add(self,class_name):
        return class_name + " { " + self.styles[class_name] + " }"
    def add_css(self):
        return "\n".join(map(self.__apply_add, self.styles.keys()))
    def __apply_fonts(self, font_link):
        return link(rel='stylesheet', href=font_link)
    def add_fonts(self):
        return [self.__apply_fonts(font) for font in self.fonts]
class ListOptions:
    def __init__(self, style="test"):
        self.style = style
def js_list(list_name: str, data: pd.DataFrame, options: ListOptions):
    """
    Python wrapper to generate a complete listjs list for displaying a pandas df.
    """
    css = CSS(options.style)

    container = div(cls="container", id=list_name)

    with container:
        css.add_fonts()
        style(css.add_css())
        br()
        search_div()
        br()
        filter_div()
        br()
        make_sort_table(data)

    td_setup = "".join(td(cls=field).render() for field in data.columns)


    options = make_options(fields=str(list(data.columns)), table_setup=td_setup)

    records = str(data.to_dict("records"))

    text_parser = make_text_parser()
    text_filter = make_filter()
    js_code = f"""var options ={options};
                  var values ={records};
                  var userList = new List('{list_name}', options, values);
                  {text_parser}
                  {text_filter};"""

    return {"html": container.render(), "js": js_code}


def make_sort_table(data):
    sort_table = table(cls="table")
    with sort_table:
        make_table_header(data)
        tbody(cls="list")
    return sort_table


def filter_div():
    cont = div(cls='container')
    with cont:
        i(cls="fas fa-search")
        input(cls="input-bar form-control", placeholder="Filter", onkeyup="filterFunction()")
    return cont

def make_table_header(data):
    return thead().add(th(field, cls="sort", data_sort=field) for field in data.columns)


def braces_wrap(base_string):
    return "{" + base_string + "}"


def make_options(fields, table_setup):
    vals = f"valueNames: {fields},\n"
    items = f"item: '<tr>{table_setup}</tr>'"
    return braces_wrap(vals + items)

def search_div():
    cont = div(cls="container")
    with cont:
        i(cls="fas fa-search")
        input(cls="input-bar search form-control", placeholder="Search")

    return cont


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
                	parsedFloat = parseFloat(filterProps[2].trim());
                    if(parsedFloat){
                        if (parseFloat(txtValue) > parsedFloat) {
                        	tr[i].style.display = "";
                    	} else {
                        	tr[i].style.display = "none";
                    	}
                    }
                    else{
                        if (txtValue.toUpperCase() > (filterProps[2].trim().toUpperCase())) {
                        	tr[i].style.display = "";
                    	} else {
                        	tr[i].style.display = "none";
                    	}
                    }
                }
                else if(filterProps[1] == '<'){
                    parsedFloat = parseFloat(filterProps[2].trim());
                    if(parsedFloat){
                        if (parseFloat(txtValue) < parsedFloat) {
                        	tr[i].style.display = "";
                    	} else {
                        	tr[i].style.display = "none";
                    	}
                    }
                    else{
                        if (txtValue.toUpperCase() < (filterProps[2].trim().toUpperCase())) {
                        	tr[i].style.display = "";
                    	} else {
                        	tr[i].style.display = "none";
                    	}
                    }
                }
            }
        }
    };"""

