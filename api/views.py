from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Ingredient, Recipe
from .serializers import IngredientSerializer

class IngredientAPIView(generics.ListAPIView):
    '''Предоставляет поиск в базе ингредиентов по их названиям.'''
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name', ]