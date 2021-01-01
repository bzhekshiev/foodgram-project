from api.models import Favorite
from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def is_favorite(value, author):
    return Favorite.objects.filter(recipe=value, author=author).exists()
