from dominate.tags import *
import pandas as pd
import json
import random

def bar_chart(name, values, limits):
    print(name)
    print(str(values))
    return """
   var ctx = document.getElementById("%s");
   var data_obj = %s
   var chart = new Chart(ctx, {
       type: 'scatter',
       data: {
           datasets: [{
               label: '',
               data: data_obj
           }]
       },
       options: {
           scales: {
                xAxes: [{
                    ticks: {
                        min: %d,
                        max: %d
                    }
                }],
                yAxes: [{
                    ticks: {
                        min: %d,
                        max: %d
                    }
                }]
           }
       }
   });
    """ % (name,str(values),limits['minX'],limits['maxX'],limits['minY'],limits['maxY'])

def js_chart(chart_name: str, data: pd.DataFrame):
    """
    Python wrapper to generate a complete listjs list for displaying a pandas df.
    """
    html_div = div(cls="container", id=chart_name)
    name = "chart"+str(random.randint(1,100000))
    with html_div:
        canvas(id=name,width="400", height="200")

    data_values = list(data.to_dict('list').values())
    labels = list(data.columns)
    js_code = bar_chart(name,
        [{'x':pair[0], 'y':pair[1]} for pair in list(zip(data_values[0],data_values[1]))],
        {
            'minX':min(data_values[0]),
            'maxX':max(data_values[0]),
            'minY':min(data_values[1]),
            'maxY':max(data_values[1])
        })

    return {"html": html_div.render(), "js": js_code}


def make_table_header(data):
    return thead().add(th(field, cls="sort", data_sort=field) for field in data.columns)

