# voter_analytics/views.py

from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter


# Create your views here.
class VotersListView(ListView):
    """
    A view to display voters information
    """

    model = Voter
    context_object_name = "voters"
    template_name = "voter_analytics/voter_list.html"
    paginate_by = 100

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()  # This gets the base queryset

        filters = self.request.GET

        # Retrieve the filters from the form
        party = filters.get("party_affiliation")
        min_year = filters.get("min_year_of_birth")
        max_year = filters.get("max_year_of_birth")
        voter_score = filters.get("voter_score")
        v20state = filters.get("v20state") == "on"
        v21town = filters.get("v21town") == "on"
        v21primary = filters.get("v21primary") == "on"
        v22general = filters.get("v22general") == "on"
        v23town = filters.get("v23town") == "on"

        # Apply filters
        if party:
            qs = qs.filter(party_affiliation=party)
        if min_year:
            qs = qs.filter(date_of_birth__year__gte=min_year)
        if max_year:
            qs = qs.filter(date_of_birth__year__lte=max_year)
        if voter_score:
            qs = qs.filter(voter_score=int(voter_score))
        if v20state:
            qs = qs.filter(v20state=True)
        if v21town:
            qs = qs.filter(v21town=True)
        if v21primary:
            qs = qs.filter(v21primary=True)
        if v22general:
            qs = qs.filter(v22general=True)
        if v23town:
            qs = qs.filter(v23town=True)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["voter_score_range"] = range(1, 6)  # Define range of voter scores
        context["year_range"] = range(1900, 2025)
        return context


class VoterDetailView(DetailView):
    """
    A view to display detailed information for a single voter
    """

    model = Voter
    context_object_name = "voter"
    template_name = "voter_analytics/voter_detail.html"
