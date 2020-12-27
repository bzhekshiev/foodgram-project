from django.contrib import admin

from .models import Ingredient, Recipe


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measure_unit')
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'description')
    list_filter = ('tag',)
    search_fields = ('title', 'author',)
    prepopulated_fields = {'slug': ('title',)}
