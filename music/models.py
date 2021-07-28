from django.db import models


class Album(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

    
class Songs(models.Model):
    name = models.CharField(max_length=128, unique=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='tracks')

    def __str__(self):
        return self.name