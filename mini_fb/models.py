# mini_fb/models.py
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    """
    Model file to represent Facebook user profile data.
    """

    # each Profile is associated to 1 User
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    email = models.EmailField()
    image_url = models.URLField()

    def __str__(self):
        """
        Return the string representation of each Fb profile,
        which is the user first and last name
        """
        return f"{self.first_name} {self.last_name}"

    def get_status_messages(self):
        """
        return a queryset of StatusMessage for which the profile is this Profile,
        and is ordered by timestamp
        """
        status_messages = StatusMessage.objects.filter(profile=self).order_by(
            "-timestamp"
        )

        return status_messages

    def get_friends(self):
        """
        return a list of the friend's profiles
        """
        friend_profiles = []

        # find the queryset of Friend objects that this profile is associated with
        friends_queryset = Friend.objects.filter(profile1=self) | Friend.objects.filter(
            profile2=self
        )

        # iterate over the friend objects queryset
        for friend in friends_queryset:
            # if profile1 is self, add profile2 to the list of friend profiles
            if (friend.profile1) == self:
                friend_profiles += [friend.profile2]
            else:
                # else, add profile1 to the list of friend profiles
                friend_profiles += [friend.profile1]

        return friend_profiles

    def add_friend(self, other):
        """
        add a Friend relation for the two Profiles: self and other
        """
        # check if self-friending
        if other == self:
            print("Sorry. Self-friending is not allowed.")
            return

        # check if friendship has existed
        friendship_count = Friend.objects.filter(
            profile1=self, profile2=other
        ) | Friend.objects.filter(profile1=other, profile2=self)
        if len(friendship_count) != 0:
            print("Friend relationship already exists.")
            return

        # otherwise, create the friend relationship
        new_friend = Friend.objects.create(profile1=self, profile2=other)
        print(f"{new_friend} have become friends.")
        return new_friend

    def get_friend_suggestions(self):
        """
        return a QuerySet of possible friends for a Profile
        the friend suggestion QuerySet should not include the current Profile,
        and not include Profiles that are already friend with the current Profile and
        """

        # get the list of friends of the current Profile
        friends = self.get_friends()

        # get the list of friend's pk
        friend_pks = [friend.pk for friend in friends]

        # get the QuerySet of possible friend suggestions
        suggestions = Profile.objects.exclude(pk__in=friend_pks).exclude(pk=self.pk)

        return suggestions

    def get_news_feed(self):
        """
        return a QuerySet of all StatusMessages for the profile on which the method was called,
        as well as all of the friends of that profile
        """
        # get the friend list of the current profile
        friends = self.get_friends()

        # add the current profile to the list of friend profiles
        newsfeed_profiles = friends + [self]

        # get the QuerySet of StatusMessage associated with the newsfeed profiles
        msgs = StatusMessage.objects.filter(profile__in=newsfeed_profiles).order_by(
            "-timestamp"
        )

        return msgs


class StatusMessage(models.Model):
    """
    Model to represent Facebook status messages for a profile
    """

    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField()
    # foreign key references a Profile
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        """
        Return the string representation for the status message
        """
        return self.message

    def get_images(self):
        """
        Get all associated images for this StatusMessage
        """
        return Image.objects.filter(status_message=self)


class Image(models.Model):
    """
    Model to represent an Image file that is related to a status message
    """

    status_message = models.ForeignKey(
        StatusMessage, on_delete=models.CASCADE, related_name="images"
    )
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return the string representation for the image
        """
        return self.image_file.url


class Friend(models.Model):
    """
    Model to represent a friend relationship between 2 profiles
    """

    profile1 = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="profile1"
    )
    profile2 = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="profile2"
    )
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return a string representation for a friend relationship between 2 profiles
        """
        profile1_fullname = self.profile1.first_name + self.profile1.last_name
        profile2_fullname = self.profile2.first_name + self.profile2.last_name
        return f"{profile1_fullname} & {profile2_fullname}"
