from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.fields import AutoCreatedField
from model_utils.models import TimeStampedModel

User = get_user_model()


class Tag(TimeStampedModel):
    name = models.CharField(_('тег'), max_length=50)
    slug = models.SlugField(max_length=20)
    color = models.CharField(_('цвет чекбокса'), max_length=20)

    class Meta:
        ordering = ['id']
        verbose_name = _('тег')
        verbose_name_plural = _('теги')

    def __str__(self):
        return self.name


class Ingredient(TimeStampedModel):
    name = models.CharField(_('название'), max_length=250, db_index=True)
    measure_unit = models.CharField(_('единица измерения'), max_length=50)

    class Meta:
        ordering = ['name']
        verbose_name = _('ингредиент')
        verbose_name_plural = _('ингредиенты')

    def __str__(self):
        return self.name


class Recipe(TimeStampedModel):
    title = models.CharField(_('название'), max_length=250, db_index=True)
    description = models.TextField(_('описание'))
    image = models.ImageField(_('картинка'), upload_to='upload')
    cooking_time = models.IntegerField(
        _('время приготовления в минутах'))
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='автор',
        related_name='recipe', db_index=True)
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient')
    tags = models.ManyToManyField(Tag, related_name='recipe_tag')

    class Meta:
        verbose_name = _('рецепт')
        verbose_name_plural = _('рецепты')
        ordering = ['-created']

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, verbose_name='рецепт', on_delete=models.CASCADE,
        related_name='recipe_cnt')
    ingredient = models.ForeignKey(
        Ingredient, verbose_name='ингредиент', on_delete=models.CASCADE)
    cnt = models.IntegerField(_('количество'))
    created = AutoCreatedField(_('дата создания'))

    class Meta:
        verbose_name = _('ингредиент рецепта')
        verbose_name_plural = _('ингредиенты рецепта')
        unique_together = ('recipe', 'ingredient')
