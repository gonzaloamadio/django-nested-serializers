from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .models import Avatar, AccessKey, Profile, User, Site, Message


class AvatarSerializer(serializers.ModelSerializer):
    image = serializers.CharField()

    class Meta:
        model = Avatar
        fields = ('pk', 'image',)


class SiteSerializer(serializers.ModelSerializer):
    url = serializers.CharField()

    class Meta:
        model = Site
        fields = ('pk', 'url',)


class AccessKeySerializer(serializers.ModelSerializer):

    class Meta:
        model = AccessKey
        fields = ('pk', 'key',)


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('pk', 'message',)


class ProfileSerializer(WritableNestedModelSerializer):
    # Direct ManyToMany relation
    sites = SiteSerializer(many=True, required=False)

    # Reverse FK relation
    avatars = AvatarSerializer(many=True, required=False)

    # Direct FK relation
    access_key = AccessKeySerializer(allow_null=True, required=False)

    # Reverse FK relation with UUID
    message_set = MessageSerializer(many=True, required=False)

    class Meta:
        model = Profile
        fields = ('pk', 'sites', 'avatars', 'access_key', 'message_set',)


class UserSerializer(WritableNestedModelSerializer):
    # Reverse OneToOne relation
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('pk', 'profile', 'username',)