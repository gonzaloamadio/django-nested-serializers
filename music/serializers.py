from rest_framework import serializers
from .models import *

"""
References:
https://stackoverflow.com/questions/26561640/django-rest-framework-read-nested-data-write-integer/39362061#39362061
https://stackoverflow.com/questions/29950956/drf-simple-foreign-key-assignment-with-nested-serializers/33048798#33048798

Best approaches for me is V9. Because we do not have to send album_id. Both read and write send and receive album field.
"""


class SongsSerializer(serializers.ModelSerializer):
    """Simple songs serializer"""

    class Meta:
        model = Songs
        fields = ("name",)


class AlbumSerializer(serializers.ModelSerializer):
    """Serializer albums. Send tracks to create them along the album

    Can post something like this:
    {
    "name": "Hybrid Theory",
    "tracks": [ {"name":"In The End"}, {"name":"Crawling"}]
    }

    """
    tracks = SongsSerializer(many=True)

    class Meta:
        model = Album
        fields = '__all__'

    def create(self, validated_data):
        album = Album.objects.create(nombre=validated_data.get("name"))
        tracks = validated_data.get('tracks')
        for track in tracks:
            Songs.objects.create(album=album, **track)
        return album


class AlbumSerializerFlat(serializers.ModelSerializer):
    """Serializer albums. Just Album fields"""
    class Meta:
        model = Album
        fields = '__all__'


class SongsNestedSerializerV1(serializers.ModelSerializer):
    """This could lead to integrity errors, because there are no PK validations. NOT RECOMMENDED"""
    album_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Songs
        fields = ("name", "album", "album_id")
        depth = 1


class SongsNestedSerializerV2(serializers.ModelSerializer):
    """This could lead to integrity errors, because there are no PK validations. NOT RECOMMENDED"""
    album_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Songs
        fields = "__all__"
        depth = 1


"""
Difference between SongsNestedSerializerV3 and SongsNestedSerializerV4 is the source field.
That is to test if the front must send album_id on V3 or can send just album.
If must send album_id, that should be fixed with source field.
"""

class SongsNestedSerializerV3(serializers.ModelSerializer):
    album_id = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Album.objects.all(), required=False, write_only=True
    )

    class Meta:
        model = Songs
        fields = "__all__"
        depth = 1


# The next 2, also work with many relationships.
# See: https://stackoverflow.com/questions/26561640/django-rest-framework-read-nested-data-write-integer/39362061#39362061  # noqa
class SongsNestedSerializerV4(serializers.ModelSerializer):
    """
    Setting source=child lets child_id act as child would by default had it not be overridden (our desired behavior).
    write_only=True makes child_id available to write to, but keeps it from showing up in the response since the id
    already shows up in the AlbumSerializer.
    REF: https://stackoverflow.com/questions/29950956/drf-simple-foreign-key-assignment-with-nested-serializers/33048798#33048798  # noqa
    """
    album_id = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Album.objects.all(), required=False, write_only=True, source='album'
    )

    class Meta:
        model = Songs
        fields = "__all__"
        depth = 1


class SongsNestedSerializerV4_1(serializers.ModelSerializer):
    class Meta:
        model = Songs
        fields = "__all__"
        depth = 1

    # override the nested item field to PrimaryKeyRelatedField on writes
    def to_internal_value(self, data):
        self.fields['album'] = serializers.PrimaryKeyRelatedField(queryset=Album.objects.all())
        return super().to_internal_value(data)


class SongsNestedSerializerV5(serializers.ModelSerializer):
    """This will expand again tracks into albums becaus of AlbumSerializer."""
    # Output expanded object
    album = AlbumSerializer(read_only=True)
    # Write ID
    album_id = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Album.objects.all(), required=False, write_only=True, source='album'
    )

    class Meta:
        model = Songs
        fields = "__all__"
        depth = 1


class SongsNestedSerializerV6(serializers.ModelSerializer):
    """Work same as V5 despite there is no depth=1"""
    album = AlbumSerializer(read_only=True)
    album_id = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Album.objects.all(), required=False, write_only=True, source='album'
    )

    class Meta:
        model = Songs
        fields = "__all__"


# TODO: Test if this work with browsable api
class SongsNestedSerializerV7(serializers.ModelSerializer):
    """REF: https://stackoverflow.com/a/39362061/1312850 """

    class Meta:
        model = Songs
        fields = "__all__"

    def to_representation(self, instance):
        self.fields['album'] = AlbumSerializer()
        return super().to_representation(instance)

    # override the nested item field to PrimaryKeyRelatedField on writes
    def to_internal_value(self, data):
        self.fields['album'] = serializers.PrimaryKeyRelatedField(queryset=Album.objects.all())
        return super().to_internal_value(data)


class SongsNestedSerializerV7Flat(serializers.ModelSerializer):
    """REF: https://stackoverflow.com/a/39362061/1312850 """

    class Meta:
        model = Songs
        fields = "__all__"

    def to_representation(self, instance):
        self.fields['album'] = AlbumSerializerFlat()
        return super().to_representation(instance)

    # override the nested item field to PrimaryKeyRelatedField on writes
    def to_internal_value(self, data):
        self.fields['album'] = serializers.PrimaryKeyRelatedField(queryset=Album.objects.all())
        return super().to_internal_value(data)


class NestedRelatedField(serializers.PrimaryKeyRelatedField):
    """
        Model identical to PrimaryKeyRelatedField but its
        representation will be nested and its input will
        be a primary key.

        Example usage:

        class PostModelSerializer(serializers.ModelSerializer):
            message = NestedRelatedField(
                 queryset=MessagePrefix.objects.all(),
                 model=MessagePrefix,
                 serializer_class=MessagePrefixModelSerializer
           )

        REF: https://stackoverflow.com/a/58504131/1312850
    """
    def __init__(self, **kwargs):
        self.pk_field = kwargs.pop('pk_field', None)
        self.model = kwargs.pop('model', None)
        self.serializer_class = kwargs.pop('serializer_class', None)
        super().__init__(**kwargs)

    def to_representation(self, data):
        pk = super().to_representation(data)
        try:
            return self.serializer_class(self.model.objects.get(pk=pk)).data
        except self.model.DoesNotExist:
            return None

    def to_internal_value(self, data):
        return serializers.PrimaryKeyRelatedField.to_internal_value(self, data)


class SongsNestedSerializerV8(serializers.ModelSerializer):
    album = NestedRelatedField(
                queryset=Album.objects.all(),
                model=Album,
                serializer_class=AlbumSerializer
           )

    class Meta:
        model = Songs
        fields = "__all__"


class RelatedFieldAlternative(serializers.PrimaryKeyRelatedField):
    """REF: https://stackoverflow.com/a/52246232/1312850

    Make this work with open api generator schema: https://stackoverflow.com/a/63612404/1312850
    Male this work with DRF templates: https://stackoverflow.com/a/64584955/1312850

    If swagger or API schema does not work. Do the 2 fields option.
    """

    def __init__(self, **kwargs):
        self.serializer = kwargs.pop('serializer', None)
        if self.serializer is not None and not issubclass(self.serializer, serializers.Serializer):
            raise TypeError('"serializer" is not a valid serializer class')

        super().__init__(**kwargs)

    def use_pk_only_optimization(self):
        return not self.serializer
        # return False if self.serializer else True

    def to_representation(self, instance):
        if self.serializer:
            return self.serializer(instance, context=self.context).data
        return super().to_representation(instance)


class SongsNestedSerializerV9(serializers.ModelSerializer):
    album = RelatedFieldAlternative(queryset=Album.objects.all(), serializer=AlbumSerializer)

    class Meta:
        model = Songs
        fields = '__all__'


class SongsNestedSerializerV9Flat(serializers.ModelSerializer):
    album = RelatedFieldAlternative(queryset=Album.objects.all(), serializer=AlbumSerializerFlat)

    class Meta:
        model = Songs
        fields = '__all__'


class SongsNestedSerializerV10(serializers.ModelSerializer):
    # This would work just as a normal PrimaryKeyRelatedField
    album = RelatedFieldAlternative(queryset=Album.objects.all())

    class Meta:
        model = Songs
        fields = '__all__'


from rest_framework.relations import PrimaryKeyRelatedField


class ModelRepresentationPrimaryKeyRelatedField(PrimaryKeyRelatedField):
    """REF: https://stackoverflow.com/a/52950172/1312850"""
    def __init__(self, **kwargs):
        self.model_serializer_class = kwargs.pop('model_serializer_class')
        super().__init__(**kwargs)

    def use_pk_only_optimization(self):
        return False

    def to_representation(self, value):
        return self.model_serializer_class(instance=value).data


class SongsNestedSerializerV11(serializers.ModelSerializer):
    album = ModelRepresentationPrimaryKeyRelatedField(
        queryset=Album.objects.all(),
        model_serializer_class=AlbumSerializer
    )

    class Meta:
        model = Songs
        fields = '__all__'


class SongsNestedSerializerV11Flat(serializers.ModelSerializer):
    album = ModelRepresentationPrimaryKeyRelatedField(
        queryset=Album.objects.all(),
        model_serializer_class=AlbumSerializerFlat
    )

    class Meta:
        model = Songs
        fields = '__all__'
