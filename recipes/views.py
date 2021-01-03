from api.models import Favorite, Purchase, Subscribe
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import requires_csrf_token

from .forms import RecipeForm
from .models import Ingredient, Recipe, Tag
from .utils import paginator_mixin, save_recipe

User = get_user_model()


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
    page, paginator = paginator_mixin(request, recipes)
    return render(
        request, 'indexAuth.html', {'page': page, 'paginator': paginator})


def recipe_view(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    return render(request, 'singlePage.html', {'recipe': recipe})


@login_required
def recipe_add(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, files=request.FILES)
        if form.is_valid():
            recipe_save = save_recipe(request, form)
            if recipe_save == 400:
                return redirect('recipe_add')
            return redirect('index')
    else:
        form = RecipeForm()
    return render(request, 'formRecipe.html', {'form': form})


@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user != recipe.author:
        return redirect('recipe_view', pk=pk)
    if request.method == 'POST':
        form = RecipeForm(request.POST or None,
                          files=request.FILES or None, instance=recipe)
        if form.is_valid():
            for tag_id in recipe.tags.all():
                recipe.tags.remove(tag_id)
            recipe.recipe_cnt.all().delete()
            recipe_save = save_recipe(request, form)
            if recipe_save == 400:
                return redirect('recipe_view', pk=pk)
            return redirect('recipe_view', pk=pk)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'formChangeRecipe.html', {'form': form, 'recipe': recipe})


@login_required
def recipe_remove(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user == recipe.author:
        recipe.delete()
        return redirect('profile', recipe.author)
    return redirect('index')


@login_required
def profile(request, username):
    recipes = Recipe.objects.filter(author__username=username)
    page, paginator = paginator_mixin(request, recipes)
    return render(request, 'authorRecipe.html', {'page': page, 'paginator': paginator})


@login_required
def favorites(request):
    recipes = Recipe.objects.filter(recipe_favorite__author=request.user)
    page, paginator = paginator_mixin(request, recipes)
    return render(request, 'favorite.html', {'page': page, 'paginator': paginator})


@login_required
def subscriptions(request):
    authors = User.objects.prefetch_related(
        'recipe').filter(following__follower=request.user).annotate(recipe_cnt=Count('recipe__id'))
    page, paginator = paginator_mixin(request, authors)
    return render(request, 'myFollow.html', {'page': page, 'paginator': paginator})


@login_required
def purchases(request):
    recipes = Recipe.objects.filter(recipe_purchase__author=request.user)
    return render(request, 'shopList.html', {'recipes': recipes})


@login_required
def purchase_remove(request, recipe_id):
    purchase = Purchase.objects.get(author=request.user, recipe__id=recipe_id)
    if request.user == purchase.author:
        purchase.delete()
        return redirect('purchases')
    return redirect('index')


@login_required
def purchase_count(request):
    return {'purchase_count': Purchase.objects.filter(author=request.user).count()}
