from django.shortcuts import render
from .lists import js_list
from .charts import js_chart
import pandas as pd
import random

# Create your views here.

def ListView(request):

    random_data = [[random.randint(1,100), random.randint(1,100)] for _ in range(10)]
    df = pd.DataFrame(random_data, columns=['a', 'b'])
    list_js = js_list("test_list", df)

    context = {
        "list":list_js
    }

    return render(request, 'lists/list_test.html', context=context)



def ChartView(request):

    random_data = [[random.randint(1,100), random.randint(1,100)] for _ in range(10)]
    df = pd.DataFrame(random_data, columns=['a', 'b'])
    chart_js = js_chart("test_chart", df)

    context = {
        "chart":chart_js
    }

    return render(request, 'charts/charts_test.html', context=context)