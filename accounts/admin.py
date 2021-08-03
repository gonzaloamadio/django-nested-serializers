from django.contrib import admin
from .models import Avatar, User, Site, Profile, AccessKey, Message

admin.site.register(Avatar)
admin.site.register(User)
admin.site.register(Site)
admin.site.register(Profile)
admin.site.register(AccessKey)
admin.site.register(Message)
