from rest_framework import viewsets
from .models import *
from .serializers import *


class AlbumViewSet(viewsets.ModelViewSet):
    model = Album
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class SongsViewSetV1(viewsets.ModelViewSet):
    model = Songs
    queryset = Songs.objects.all()
    serializer_class = SongsNestedSerializerV1


class SongsViewSetV2(viewsets.ModelViewSet):
    model = Songs
    queryset = Songs.objects.all()
    serializer_class = SongsNestedSerializerV2


class SongsViewSetV3(viewsets.ModelViewSet):
    model = Songs
    queryset = Songs.objects.all()
    serializer_class = SongsNestedSerializerV3


class SongsViewSetV4(viewsets.ModelViewSet):
    model = Songs
    queryset = Songs.objects.all()
    serializer_class = SongsNestedSerializerV4


class SongsViewSetV5(viewsets.ModelViewSet):
    model = Songs
    queryset = Songs.objects.all()
    serializer_class = SongsNestedSerializerV5


class SongsViewSetV6(viewsets.ModelViewSet):
    model = Songs
    queryset = Songs.objects.all()
    serializer_class = SongsNestedSerializerV6


class SongsViewSetV7(viewsets.ModelViewSet):
    model = Songs
    queryset = Songs.objects.all()
    serializer_class = SongsNestedSerializerV7


class SongsViewSetV8(viewsets.ModelViewSet):
    model = Songs
    queryset = Songs.objects.all()
    serializer_class = SongsNestedSerializerV8


class SongsViewSetV9(viewsets.ModelViewSet):
    model = Songs
    queryset = Songs.objects.all()
    serializer_class = SongsNestedSerializerV9


class SongsViewSetV10(viewsets.ModelViewSet):
    model = Songs
    queryset = Songs.objects.all()
    serializer_class = SongsNestedSerializerV10


class SongsViewSetV11(viewsets.ModelViewSet):
    model = Songs
    queryset = Songs.objects.all()
    serializer_class = SongsNestedSerializerV11

