# voter_analytics/urls.py

from django.urls import path
from . import views

app_name = "voter_analytics"

urlpatterns = [
    path(r"", views.VotersListView.as_view(), name="home"),
    path(r"voters/", views.VotersListView.as_view(), name="voters"),
    path("voter/<int:pk>/", views.VoterDetailView.as_view(), name="voter"),
]
