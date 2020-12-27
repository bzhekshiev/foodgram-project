from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .models import Ingredient, Recipe


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )

def server_error(request):
    return render(request, 'misc/500.html', status=500)

def index(request): 
    recipes = Recipe.objects.order_by('-created').all() 
    paginator = Paginator(recipes, 6) 
    page_number = request.GET.get('page') 
    page = paginator.get_page(page_number) 
    return render( 
        request, 'indexAuth.html', {'page': page, 'paginator': paginator})

def recipe_add(request):
    return render(request,'formRecipe.html')


def shop_list(request):
    return render(request, 'shopList.html')
