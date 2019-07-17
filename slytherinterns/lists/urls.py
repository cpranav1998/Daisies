from django.urls import path
from . import views

urlpatterns = [path("", views.ListView, name="list-view")]
