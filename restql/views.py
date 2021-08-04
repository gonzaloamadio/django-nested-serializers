from rest_framework import viewsets
from .models import *
from .serializers import *


class ProductViewSet(viewsets.ModelViewSet):
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    model = Ingredient
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class IngredientMixViewSet(viewsets.ModelViewSet):
    model = IngredientMix
    queryset = IngredientMix.objects.all()
    serializer_class = IngredientMixSerializer
