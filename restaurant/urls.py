from django.urls import path
from . import views

app_name = "restaurant"

urlpatterns = [
    path(r"", views.main, name="main"),
    path(r"main/", views.main, name="main"),
    path(r"order", views.order, name="order"),
    path(r"confirmation/", views.confirmation, name="confirmation"),
]
