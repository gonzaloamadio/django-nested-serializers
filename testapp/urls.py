from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from music.views import *
from accounts.views import *

router = DefaultRouter()

# Music routes
# router.register(r'albums', AlbumViewSet)
# router.register(r'songsv1', SongsViewSetV1)
# router.register(r'songsv2', SongsViewSetV2)
# router.register(r'songsv3', SongsViewSetV3)
# router.register(r'songsv4', SongsViewSetV4)
# router.register(r'songsv41', SongsViewSetV4_1)
# router.register(r'songsv5', SongsViewSetV5)
# router.register(r'songsv6', SongsViewSetV6)
# router.register(r'songsv7', SongsViewSetV7)
# router.register(r'songsv7flat', SongsViewSetV7Flat)
# router.register(r'songsv8', SongsViewSetV8)
# router.register(r'songsv9', SongsViewSetV9)
# router.register(r'songsv9flat', SongsViewSetV9Flat)
# router.register(r'songsv10', SongsViewSetV10)
# router.register(r'songsv11', SongsViewSetV11)
# router.register(r'songsv11flat', SongsViewSetV11Flat)

# Account Routes
router.register(r'sites', SiteViewSet)
router.register(r'users', UserViewSet)
router.register(r'acceskeys', ProfileViewSet)
router.register(r'avatars', AvatarViewSet)
router.register(r'profiles', ProfileViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
