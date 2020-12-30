from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.recipe_add, name='recipe_add'),
    path('shop_list', views.shop_list, name='shop_list'),

]
