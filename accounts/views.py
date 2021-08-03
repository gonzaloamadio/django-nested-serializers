from rest_framework import viewsets
from .models import *
from .serializers import *


class SiteViewSet(viewsets.ModelViewSet):
    model = Site
    queryset = Site.objects.all()
    serializer_class = SiteSerializer


class UserViewSet(viewsets.ModelViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AccessKeyViewSet(viewsets.ModelViewSet):
    model = AccessKey
    queryset = AccessKey.objects.all()
    serializer_class = AccessKeySerializer


class ProfileViewSet(viewsets.ModelViewSet):
    model = Profile
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class AvatarViewSet(viewsets.ModelViewSet):
    model = Avatar
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer

