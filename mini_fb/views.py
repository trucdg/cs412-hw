from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)
from .models import Profile, StatusMessage, Image
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404


from django.contrib.auth.models import User


# Create your views here.
class ShowAllProfilesView(ListView):
    """
    A view class to display all profiles stored in the Profile model
    """

    # Specify the model to be listed in the view
    model = Profile

    # the template that will be used to display the profile data
    template_name = "mini_fb/show_all_profiles.html"

    # the name of the object manager that store all profiles
    context_object_name = "profiles"


class ShowProfilePageView(DetailView):
    """
    A view class to display a single profile page
    """

    model = Profile

    template_name = "mini_fb/show_profile.html"

    context_object_name = "profile"


class ShowProfileForUser(DetailView):
    """
    A view class to display the profile page for the current user
    """

    model = Profile

    template_name = "mini_fb/show_profile.html"

    context_object_name = "profile"

    def get_object(self, queryset=None):
        # Fetch the profile based on the logged-in user
        # to resolve the problem where multiple existing profiles are connected to the test user
        # use filter instead of get, then return only 1 profile
        profile = Profile.objects.filter(user=self.request.user)[0]
        return profile


class CreateProfileView(CreateView):
    """
    a class inherits from the generic CreateView class
    handles request to URL: '/mini_fb/create_profile/'
    - on GET: returns a form to create a Profile instance
    - on POST: process and validate the form,
               then create and save the new Profile,
               then redirect to the DetailView of this Profile

    """

    # Specify the form that this view use
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

    def form_valid(self, form):
        """
        This method is called after the form is validated
        before saving the data to the database
        """
        print(f"CreateProfileView.form_valid(): form={form.cleaned_data}")
        print(f"CreateProfileView.form_valid(): self.kwargs={self.kwargs}")

        return super().form_valid(form)

    def form_invalid(self, form):
        """
        this method is called when the form is invalid
        """
        print(f"CreateProfileView.form_invalid(): form={form.cleaned_data}")
        print(f"CreateProfileView.form_invalid(): self.kwargs={self.kwargs}")
        return super().form_invalid(form)

    def get_success_url(self) -> str:
        """
        return the URL to redirect on success
        """
        return reverse("mini_fb:show_profile", kwargs={"pk": self.object.pk})


class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    """
    A class inherits from the CreateView django generic view
    handles request to URL /mini_fb/profile/<int:pk>/create_status
    on GET: return a form to create a StatusMessage instance
    on POST: validate the form, save data and redirect to the Profile detail view
    """

    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_login_url(self) -> str:
        """
        return the URL of the login page
        """
        return reverse("mini_fb:login")

    def form_valid(self, form):
        """
        this method is called when the form is valid, and before saving data to database
        """
        print(f"CreateStatusMessageView.form_valid(): form={form.cleaned_data}")
        print(f"CreateStatusMessageView.form_valid(): self.kwargs={self.kwargs}")
        print(f"CreateStatusMessageView.form_valid(): self.request={self.request}")
        print(
            f"CreateStatusMessageView.form_valid(): self.request.user={self.request.user}"
        )

        # find the Profile specified by the kwargs obtained by the URL
        # profile = Profile.objects.get(pk=self.kwargs["pk"])

        # if profile.user != self.request.user:
        #    raise PermissionDenied("You are not the profile owner.")

        # Attach the StatusMessage instance created by the form to the profile
        profile = Profile.objects.get(user=self.request.user)
        form.instance.profile = profile

        # Save the StatusMessage to the db
        sm = form.save()

        # Read the files from the form
        files = self.request.FILES.getlist("files")

        # for each file, create an Image object and save it
        for f in files:
            # create a new Image object
            img = Image()
            img.image_file = f  # assign the uploaded file
            img.status_message = sm
            img.save()  # save to db
            print(
                f"CreateStatusMessageView.form_valid(): Saved image: {img.image_file}"
            )

        return super().form_valid(form)

    def form_invalid(self, form):
        """
        this method is called when the form is invalid
        used for debugging purpose
        """
        print(f"CreateStatusMessageView.form_invalid(): form={form.cleaned_data}")
        print(f"CreateStatusMessageView.form_invalid(): self.kwargs={self.kwargs}")
        return super().form_invalid(form)

    def get_success_url(self):
        """
        return the URL on success
        """
        # find the Profile associated with the pk specified by the kwargs obtained by the URL
        # profile = Profile.objects.get(self.kwargs['pk'])
        return reverse("mini_fb:show_profile_for_user")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        provide extra context data to the template
        """

        # first, get all the context data from the super class
        context = super().get_context_data(**kwargs)

        # find the Profile identifies by the PK specified by the URL pattern
        # profile = Profile.objects.get(pk=self.kwargs["pk"])

        profile = Profile.objects.filter(user=self.request.user)[0]

        # add the Profile into the context
        context["profile"] = profile

        # return the context to be used by the template
        return context


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """
    A view to update a Profile and save it to database
    """

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

    def get_login_url(self) -> str:
        """
        return the URL of the login page
        """
        return reverse("mini_fb:login")

    def form_valid(self, form):
        """
        Handles form submission after form is validated
        """

        print(f"UpdateProfileView.form_valid(): form.cleaned_data={form.cleaned_data}")
        return super().form_valid(form)

    def get_success_url(self):
        """
        Redirect to the show_profile page after successful update
        """

        return reverse("mini_fb:show_profile_for_user")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        provide extra context data to the template
        """

        # first, get all the context data from the super class
        context = super().get_context_data(**kwargs)

        # find the Profile identifies by the PK specified by the URL pattern
        # profile = Profile.objects.get(pk=self.kwargs["pk"])

        # get the profile associated with the current login user
        user = self.request.user

        profile = Profile.objects.get(user=user)

        # add the Profile into the context
        context["profile"] = profile

        # return the context to be used by the template
        return context

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        # get the profile associated with current user
        # use filter to deal with the problem where the test user are associated with
        # multiple profiles
        profile = Profile.objects.filter(user=self.request.user)[0]
        return profile


class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    """
    A view to delete a StatusMessage and remove it from the database
    """

    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"
    context_object_name = "status_message"

    def get_login_url(self) -> str:
        """
        return the URL of the login page
        """
        return reverse("mini_fb:login")

    def get_success_url(self):
        # After successful deletion, redirect back to the Profile page
        profile_id = self.object.profile.id
        return reverse("mini_fb:show_profile_for_user")


class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    """
    A view class to update the StatusMessage
    """

    model = StatusMessage
    fields = ["message"]
    template_name = "mini_fb/update_status_form.html"
    context_object_name = "status_message"

    def get_login_url(self) -> str:
        """
        return the URL of the login page
        """
        return reverse("mini_fb:login")

    def get_success_url(self):
        # After a successful update, redirect back to the Profile page
        profile_id = self.object.profile.id
        return reverse("mini_fb:show_profile", kwargs={"pk": profile_id})


class CreateFriendView(View):
    """
    A view class to handle Friendship creation
    """

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        override the dispatch method to get URL parameters and Profile objects
        """
        # get URL parameters
        # pk = self.kwargs["pk"]
        other_pk = self.kwargs["other_pk"]

        # get the profile associated with the current user
        p1 = Profile.objects.filter(user=self.request.user)[0]

        # get the profiles using the pk
        # p1 = Profile.objects.get(pk=pk)
        p2 = Profile.objects.get(pk=other_pk)

        # create the Friend relationship
        p1.add_friend(p2)

        return redirect(reverse("mini_fb:show_profile_for_user"))


class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    """
    A view class to show friend suggestions
    """

    model = Profile
    template_name = "mini_fb/friend_suggestions.html"
    context_object_name = "profile"

    def get_login_url(self) -> str:
        """
        return the URL of the login page
        """
        return reverse("mini_fb:login")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        return a context dictionary to give friend suggestion data to the template
        """
        context = super().get_context_data(**kwargs)
        context["suggestions"] = self.object.get_friend_suggestions()

        return context

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        # get the profile associated with current user
        # use filter to deal with the problem where the test user are associated with
        # multiple profiles
        profile = Profile.objects.filter(user=self.request.user)[0]
        return profile


class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "mini_fb/news_feed.html"
    context_object_name = "profile"

    def get_login_url(self) -> str:
        """
        return the URL of the login page
        """
        return reverse("mini_fb:login")

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        # get the profile object associated with this current user
        # use filter method to resolve the problem where the test user is associated with
        # multiple profiles
        profile = Profile.objects.filter(user=self.request.user)[0]

        return profile

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        return a context dictionary to give newsfeed data to the template
        """
        context = super().get_context_data(**kwargs)

        # get newsfeed for the current profile
        context["news_feed"] = self.object.get_news_feed()

        return context
