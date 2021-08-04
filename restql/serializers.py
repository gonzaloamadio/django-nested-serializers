from django_restql.fields import NestedField
from django_restql.mixins import DynamicFieldsMixin
from django_restql.serializers import NestedModelSerializer
from rest_framework import serializers

from .models import Product, Ingredient, IngredientMix


class IngredientSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']


class IngredientMixSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    ingredient = NestedField(IngredientSerializer, accept_pk_only=True)

    class Meta:
        model = IngredientMix
        fields = ['id', 'ingredient', 'product']


class ProductSerializer(DynamicFieldsMixin, NestedModelSerializer):

    # Ref: https://yezyilomo.github.io/django-restql/mutating_data/#using-dynamicfieldsmixin-and-nestedfield-together
    # Many is true, because this is the reversed relation.
    ingredient_mixes = NestedField(IngredientMixSerializer, many=True, required=False)

    class Meta:
        model = Product
        fields = '__all__'
