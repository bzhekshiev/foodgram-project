
from recipes.models import Ingredient, Recipe
from rest_framework import serializers

from api.models import Favorite


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class FavoriteSerializer(serializers.ModelSerializer):

    id = serializers.SlugRelatedField(
        slug_field='id', queryset=Recipe.objects.all(), source='recipe')
    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('id', 'author')
        model = Favorite

    def create(self, validated_data):
        if 'author' not in validated_data:
            validated_data['author'] = self.context['request'].user
        return Favorite.objects.create(**validated_data)
