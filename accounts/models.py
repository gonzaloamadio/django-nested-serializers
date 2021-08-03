"""
Models used to test package: https://github.com/beda-software/drf-writable-nested
"""
# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError


def validate_dummy(value):
    if value == "err_value":
        raise ValidationError("Error value")


class Site(models.Model):
    url = models.CharField(max_length=100, validators=[validate_dummy])


class User(models.Model):
    username = models.CharField(max_length=100, validators=[validate_dummy])


class AccessKey(models.Model):
    key = models.CharField(max_length=100, validators=[validate_dummy])


class Profile(models.Model):
    sites = models.ManyToManyField(Site)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_key = models.ForeignKey(AccessKey, null=True, on_delete=models.CASCADE)


class Avatar(models.Model):
    image = models.CharField(max_length=100, validators=[validate_dummy])
    profile = models.ForeignKey(Profile, related_name='avatars', on_delete=models.CASCADE)


class Message(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
