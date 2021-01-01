from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from recipes.models import Ingredient, Recipe
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Favorite

from .serializers import IngredientSerializer, FavoriteSerializer


class CreateResponseMixin:
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"success": True})
        return Response({"success": False})


class IngredientAPIView(generics.ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name', ]


class FavoriteAdd(CreateResponseMixin, generics.CreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
