from django.urls import path
from . import views


urlpatterns = [
    path('view/<int:pk>/', views.recipe_view, name='recipe_view'),
    path('author/<str:username>/', views.profile, name='profile'),
    path('favorites', views.favorite, name='favorite'),
    path('shop_list', views.shop_list, name='shop_list'),
    path('add', views.recipe_add, name='recipe_add'),
    path('', views.index, name='index'),
]
