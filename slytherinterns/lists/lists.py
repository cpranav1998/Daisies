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
    html_div = div(cls="container", id=list_name)
    print(css.add_fonts())
    with html_div:
        css.add_fonts()
        style(css.add_css())
        div(input(cls="search form-control", placeholder="Search"), cls="container")
        br()
        tbl = table(cls="table")
        with tbl:
            make_table_header(data)
            tbody(cls="list")

    td_setup = "".join(td(cls=field).render() for field in data.columns)

    table_options = """
            {{valueNames: {fields},
            item: '<tr class="item">{table_setup}</tr>'
            }}""".format(
        fields=str(list(data.columns)), table_setup=td_setup
    )

    js_code = """
                let options ={td_setup};
                let values ={records};
                let userList = new List('{list_name}', options, values);
            """.format(
        td_setup=table_options, records=str(data.to_dict("records")), list_name=list_name
    )

    return {"html": html_div.render(), "js": js_code}


def make_table_header(data):
    return thead().add(th(field, cls="sort", data_sort=field) for field in data.columns)

