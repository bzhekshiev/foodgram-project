from decimal import Decimal

from django.core.paginator import Paginator
from django.db import IntegrityError, transaction

from .models import Ingredient, RecipeIngredient


def save_recipe(request, form):
    '''Функция сохраняет данные при создании и редактировании рецепта.'''
    try:
        with transaction.atomic():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            for tag in form.cleaned_data['tags']:
                recipe.tags.add(tag.id)

            ingredients = []
            for key, value in form.data.items():
                if 'nameIngredient' in key:
                    name = value
                elif 'valueIngredient' in key:
                    cnt = Decimal(value.replace(',', '.'))
                elif 'unitsIngredient' in key:
                    measure_unit = value
                    ingredient = Ingredient.objects.get(
                        name=name, measure_unit=measure_unit)
                    ingredients.append(
                        RecipeIngredient(
                            ingredient=ingredient, recipe=recipe, cnt=cnt)
                    )
            RecipeIngredient.objects.bulk_create(ingredients)
            return None
    except IntegrityError:
        return 400


def paginator_mixin(request, queryset):
    paginator = Paginator(queryset, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page, paginator
