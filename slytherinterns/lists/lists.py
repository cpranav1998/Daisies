from dominate.tags import *
import pandas as pd


def js_list(list_name: str, data: pd.DataFrame):
    """
    Python wrapper to generate a complete listjs list for displaying a pandas df.
    """

    html_div = div(cls="container", id=list_name)
    with html_div:
        br()
        div(input(cls="search form-control", placeholder="Search"), cls="container")
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

    js_code = """var options ={td_setup}; 
                var values ={records};
                var userList = new List('{list_name}', options, values);""".format(
        td_setup=options, records=str(data.to_dict("records")), list_name=list_name
    )

    return {"html": html_div.render(), "js": js_code}


def make_table_header(data):
    return thead().add(th(field, cls="sort", data_sort=field) for field in data.columns)

