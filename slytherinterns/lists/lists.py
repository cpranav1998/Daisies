from dominate.tags import *
import pandas as pd
import json

class CSS:
    def __init__(self, name: str):
        with open('./css/{name}.json') as json_file:
            self.styles = json.load(json_file)

    def add_css(self):
        add = lambda class_name: class_name + " { " self.styles[class_name] + " } "
        return "\n".join(map(lambda el: add(el),self.styles.keys()))


def js_list(list_name: str, data: pd.DataFrame, options={}):
    """
    Python wrapper to generate a complete listjs list for displaying a pandas df.
    """
    css = CSS(options.style)
    html_div = div(cls="container", id=list_name)
    with html_div:
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

