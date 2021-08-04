from django.db import models
from django.core.exceptions import ValidationError


def validate_dummy(value):
    if value == "err_value":
        raise ValidationError("Error value")


class Product(models.Model):
    name = models.CharField(max_length=100, validators=[validate_dummy])


class Ingredient(models.Model):
    name = models.CharField(max_length=100, validators=[validate_dummy])


class IngredientMix(models.Model):
    ingredient = models.ForeignKey(Ingredient, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE, related_name='ingredient_mixes')

    class Meta:
        unique_together = (('ingredient', 'product'),)
