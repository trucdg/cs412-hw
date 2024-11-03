from django.contrib import admin
from .models import Profile, StatusMessage, Image, Friend

# Register your models here.
# Register Profile model so that it can be managed through the Django Admin interface
admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)
admin.site.register(Friend)
