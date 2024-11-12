# voter_analytics/views.py

from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
import plotly
import plotly.graph_objs as go


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


class GraphsListView(ListView):
    """
    A view to display graphs of voters
    """

    model = Voter
    template_name = "voter_analytics/graphs.html"
    context_object_name = "voters"

    def get_queryset(self):
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
        """
        Provide context variables and graphs to use in templates
        """
        context = super().get_context_data(**kwargs)

        # Graph 1: Distribution of Voters by Year of Birth (Histogram)
        birth_years = [v.date_of_birth.year for v in context["voters"]]
        year_dist = go.Histogram(x=birth_years, nbinsx=100, name="Year of Birth")
        year_dist_layout = go.Layout(title="Distribution of Voters by Year of Birth")
        graph_div_birth_years = plotly.offline.plot(
            {"data": [year_dist], "layout": year_dist_layout},
            auto_open=False,
            output_type="div",
        )
        context["graph_div_birth_years"] = graph_div_birth_years

        # Graph 2: Distribution of Voters by Party Affiliation (Pie Chart)
        # party_count = (
        #     context["voters"]
        #     .values("party_affiliation")
        #     .annotate(count=Count("party_affiliation"))
        # )
        # labels = [party["party_affiliation"] for party in party_count]
        # values = [party["count"] for party in party_count]
        # party_dist = go.Pie(
        #     labels=labels,
        #     values=values,
        #     title="Voter Distribution by Party Affiliation",
        # )
        # graph_div_party_affiliation = plotly.offline.plot(
        #     {"data": [party_dist]}, auto_open=False, output_type="div"
        # )
        # context["graph_div_party_affiliation"] = graph_div_party_affiliation

        # Graph 3: Distribution of Voters by Participation in Elections (Histogram)
        # election_columns = [
        #     "v20state",
        #     "v21town",
        #     "v21primary",
        #     "v22general",
        #     "v23town",
        # ]
        # election_participation = [
        #     sum([getattr(v, col) for col in election_columns])
        #     for v in context["voters"]
        # ]
        # election_dist = go.Histogram(
        #     x=election_participation, nbinsx=5, name="Election Participation"
        # )
        # election_dist_layout = go.Layout(title="Voter Participation in Elections")
        # graph_div_election_participation = plotly.offline.plot(
        #     {"data": [election_dist], "layout": election_dist_layout},
        #     auto_open=False,
        #     output_type="div",
        # )
        # context["graph_div_election_participation"] = graph_div_election_participation

        return context
