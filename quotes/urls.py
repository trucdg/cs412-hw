from django.urls import path
from . import views

# Define the URL patterns for the quotes app.
# Each URL pattern maps to a view function in views.py
app_name = "quotes"

urlpatterns = [
    path(r"", views.quote, name="quote"),
    path(r"quote/", views.quote, name="quote"),
    path(r"show_all/", views.show_all, name="show_all"),
    path(r"about/", views.about, name="about"),
]
