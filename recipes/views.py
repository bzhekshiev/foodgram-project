from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import requires_csrf_token

from .forms import RecipeForm
from .models import Ingredient, Recipe, Tag
from .utils import save_recipe


@requires_csrf_token
def page_bad_request(request, exception):
    return render(request, "misc/400.html", {"path": request.path}, status=400)


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
    recipes = Recipe.objects.all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, 'indexAuth.html', {'page': page, 'paginator': paginator})



def recipe_view(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    print(recipe)
    return render(request, 'singlePage.html',{'recipe':recipe})

@login_required
def recipe_add(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, files=request.FILES)
        if form.is_valid():
            recipe_save = save_recipe(request, form)
            if recipe_save == 400:
                return redirect('add')
            return redirect('index')
    else:
        form = RecipeForm()
    return render(request, 'formRecipe.html', {'form': form})

def profile(request, username):
    recipes = Recipe.objects.filter(author__username=username)
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,'authorRecipe.html',{'page': page, 'paginator': paginator})

def shop_list(request):
    return render(request, 'shopList.html')
