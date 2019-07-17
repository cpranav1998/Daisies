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
        sort_table = table(cls="table")
        with sort_table:
            make_table_header(data)
            tbody(cls="list")

    td_setup = "".join(td(cls=field).render() for field in data.columns)

    options = make_options(fields=str(list(data.columns)), table_setup=td_setup)

    records = str(data.to_dict("records"))

    js_code = f"""var options ={options};
                var values ={records};
                var userList = new List('{list_name}', options, values);"""

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