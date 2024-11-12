# voter_analytics/views.py

from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
from collections import Counter
from django.db.models import Count
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
        context["voter_score_range"] = range(1, 6)  # Define range of voter scores
        context["year_range"] = range(1900, 2025)

        # get the filtered data
        qs = self.get_queryset()

        # Graph 1: Distribution of Voters by Year of Birth (Bar)

        # Get all Voter records' year of birth
        all_birth_years = qs.values_list("date_of_birth__year", flat=True)

        # Count the number of voters for each year using Counter (this is a Pythonic way)
        birth_year_counts = Counter(all_birth_years)

        # Prepare the data for plotting
        x1 = sorted(birth_year_counts.keys())  # sorted list of years
        y1 = [birth_year_counts[year] for year in x1]  # corresponding counts

        total_voters = sum(y1)
        title1 = f"Voter Birth Year Distribution (n = {total_voters})"

        # Create a bar chart
        year_dist = go.Bar(x=x1, y=y1)
        year_dist_layout = go.Layout(
            title=title1,
            xaxis=dict(title="Birth Year"),
            yaxis=dict(title="Number of Voters"),
            width=1000,
            height=800,
        )

        # Convert the graph to a div
        graph_div_birth_years = plotly.offline.plot(
            {"data": [year_dist], "layout": year_dist_layout},
            auto_open=False,
            output_type="div",
        )

        context["graph_div_birth_years"] = graph_div_birth_years

        # Graph 2: Distribution of Voters by Party Affiliation (Pie)

        # Get all Voter records' party affiliations
        all_party_affiliations = qs.values_list("party_affiliation", flat=True)

        # Count the number of voters for each party using Counter
        party_counts = Counter(all_party_affiliations)

        # Prepare the data for the pie chart
        labels = list(party_counts.keys())  # party affiliations
        values = [party_counts[party] for party in labels]  # corresponding counts

        total_voters = sum(values)
        title2 = f"Voter Distribution by Party Affiliation (n = {total_voters})"

        # Create a pie chart
        party_dist = go.Pie(
            labels=labels,
            values=values,
        )
        party_dist_layout = go.Layout(title=title2, width=1000, height=800)

        # Convert the graph to a div
        graph_div_party_affiliation = plotly.offline.plot(
            {"data": [party_dist], "layout": party_dist_layout},
            auto_open=False,
            output_type="div",
        )
        context["graph_div_party_affiliation"] = graph_div_party_affiliation

        # Graph 3: Distribution of Voters by Participation in Elections (Histogram)

        # Get voter participation counts for each election
        v20state_count = qs.filter(v20state=True).count()
        v21town_count = qs.filter(v21town=True).count()
        v21primary_count = qs.filter(v21primary=True).count()
        v22general_count = qs.filter(v22general=True).count()
        v23town_count = qs.filter(v23town=True).count()

        # set up the x and y data
        x3 = [
            "v20state",
            "v21town",
            "v21primary",
            "v22general",
            "v23town",
        ]

        y3 = [
            v20state_count,
            v21town_count,
            v21primary_count,
            v22general_count,
            v23town_count,
        ]

        title3 = f"Voter Count by Election (n = {total_voters})"

        # create the graph
        election_dist = go.Bar(x=x3, y=y3)
        election_dist_layout = go.Layout(
            title=title3,
            xaxis_title="Election",
            yaxis_title="Number of Voters",
            width=1000,
            height=800,
        )

        graph_div_election_participation = plotly.offline.plot(
            {"data": [election_dist], "layout": election_dist_layout},
            auto_open=False,
            output_type="div",
        )
        context["graph_div_election_participation"] = graph_div_election_participation

        return context
