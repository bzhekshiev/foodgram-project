from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.fields import AutoCreatedField
from model_utils.models import TimeStampedModel

User = get_user_model()


class TagType(models.TextChoices):
    BREAKFAST = 'breakfast', _('завтрак')
    LUNCH = 'lunch', _('обед')
    DINNER = 'dinner', _('ужин')


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
        _('время приготовления в минутах'), default=0)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name = 'автор', related_name='recipe', db_index=True)
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient')
    tag = models.CharField(_('тег'), max_length=20,
                           choices=TagType.choices, db_index=True)
    slug = models.SlugField(max_length=300)

    class Meta:
        verbose_name = _('рецепт')
        verbose_name_plural = _('рецепты')

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    cnt = models.IntegerField(_('количество'))
    created = AutoCreatedField(_('дата создания'))

    class Meta:
        verbose_name = _('ингредиент рецепта')
        verbose_name_plural = _('ингредиенты рецепта')
        unique_together = ('recipe', 'ingredient')
