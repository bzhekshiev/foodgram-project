from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.fields import AutoCreatedField
from recipes.models import Recipe

User = get_user_model()


class Favorite(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор', related_name='author_favorite')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='рецепт', related_name='recipe_favorite')

    class Meta:
        unique_together = ('author','recipe')
        verbose_name = _('избранное')
        verbose_name_plural = _('избранные')