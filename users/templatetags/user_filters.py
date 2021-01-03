import re

from api.models import Favorite, Purchase, Subscribe
from django import template

try:
    from django.urls import NoReverseMatch, reverse
except ImportError:
    from django.core.urlresolvers import NoReverseMatch, reverse
register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def is_favorite(value, author):
    return Favorite.objects.filter(recipe=value, author=author).exists()


@register.filter
def is_purchase(value, author):
    return Purchase.objects.filter(recipe=value, author=author).exists()


@register.filter
def is_subscribe(value, follower):
    return Subscribe.objects.filter(
        author=value, follower=follower
    ).exists()


@ register.simple_tag(takes_context=True)
def active(context, pattern_or_urlname):
    try:
        pattern=reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern=pattern_or_urlname
    path=context['request'].path
    if pattern == path:
        return 'nav__item_active'
    return ''
