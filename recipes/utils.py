from decimal import Decimal

from django.db import IntegrityError, transaction

from .models import Ingredient, Recipe, RecipeIngredient, Tag


def save_recipe(request, form):
    '''Функция сохраняет данные при создании и редактировании рецепта.'''
    try:
        with transaction.atomic():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            for tag_id in request.POST.getlist('tags'):
                tag = Tag.objects.get(pk=tag_id)
                recipe.tags.add(tag)

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
                            ingredient=ingredient, recipe=recipe,cnt=cnt)
                    )
            RecipeIngredient.objects.bulk_create(ingredients)
            return None
    except IntegrityError:
        return 400
