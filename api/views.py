from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from recipes.models import Ingredient, Recipe
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Favorite, Purchase, Subscribe

from .serializers import (FavoriteSerializer, IngredientSerializer,
                          PurchaseSerializer, SubscribeSerializer)

User = get_user_model()


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


class FavoriteDelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        favorite = recipe.recipe_favorite.filter(author=request.user)
        if favorite.delete():
            return Response({"success": True})
        return Response({"success": False})


class SubscribeAdd(CreateResponseMixin, generics.CreateAPIView):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated]


class SubscribeDelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        author = get_object_or_404(User, id=id)
        subscribe = author.following.filter(follower=request.user)
        if subscribe.delete():
            return Response({"success": True})
        return Response({"success": False})


class PurchaseAdd(CreateResponseMixin, generics.CreateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]


class PurchaseDelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        purchase = recipe.recipe_purchase.filter(author=request.user)
        if purchase.delete():
            return Response({"success": True})
        return Response({"success": False})
