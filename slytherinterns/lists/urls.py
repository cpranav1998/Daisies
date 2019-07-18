from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.ListView, name="list-view"),
    path("chart/", views.ChartView, name="chart-view")
]
