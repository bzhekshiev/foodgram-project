from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient, Tag


class IngredientnlineAdmin(admin.TabularInline):
    model = RecipeIngredient
    autocomplete_fields = ('ingredient',)
    extra = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measure_unit')
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'description')
    list_filter = ('tags',)
    inlines = (IngredientnlineAdmin, )
    list_per_page = 20
    search_fields = ('title', 'author',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', )
