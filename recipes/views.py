from api.models import Purchase
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm
from .models import Recipe, Tag
from .utils import paginator_mixin, save_recipe

User = get_user_model()


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
    tags = request.GET.getlist('tags')
    if tags:
        recipes = Recipe.objects.prefetch_related(
            'author', 'tags'
        ).filter(
            tags__slug__in=tags
        ).distinct()
    else:
        recipes = Recipe.objects.all()
    all_tags = Tag.objects.all()
    page, paginator = paginator_mixin(request, recipes)
    return render(
        request, 'indexAuth.html',
        {'page': page, 'paginator': paginator, 'all_tags': all_tags})


def recipe_view(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'singlePage.html', {'recipe': recipe})


@login_required
def recipe_add(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, files=request.FILES)

        if 'nameIngredient_1' not in request.POST:
            form.add_error(None, 'Внесите ингредиенты, пожалуйста!')

        if form.is_valid():
            recipe_save = save_recipe(request, form)
            if recipe_save == 400:
                return redirect('page_bad_request')
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

        if 'nameIngredient_1' not in request.POST:
            form.add_error(None, 'Внесите ингредиенты, пожалуйста!')

        if form.is_valid():
            for tag_id in recipe.tags.all():
                recipe.tags.remove(tag_id)
            recipe.recipe_cnt.all().delete()
            recipe_save = save_recipe(request, form)
            if recipe_save == 400:
                return redirect('page_bad_request')
            return redirect('recipe_view', pk=pk)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'formChangeRecipe.html',
                  {'form': form, 'recipe': recipe})


@login_required
def recipe_remove(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user == recipe.author:
        recipe.delete()
        return redirect('profile', recipe.author)
    return redirect('index')


def profile(request, username):
    recipes = Recipe.objects.filter(author__username=username)
    page, paginator = paginator_mixin(request, recipes)
    return render(request, 'authorRecipe.html',
                  {'page': page, 'paginator': paginator})


@login_required
def favorites(request):
    tags = request.GET.getlist('tags')
    if tags:
        recipes = Recipe.objects.filter(
            recipe_favorite__author=request.user).prefetch_related(
            'author', 'tags').filter(
            tags__slug__in=tags).distinct()
    else:
        recipes = Recipe.objects.filter(recipe_favorite__author=request.user)
    all_tags = Tag.objects.all()
    page, paginator = paginator_mixin(request, recipes)
    return render(
        request, 'favorite.html',
        {'page': page, 'paginator': paginator, 'all_tags': all_tags})


@login_required
def subscriptions(request):
    authors = User.objects.prefetch_related('recipe').filter(
        following__follower=request.user).annotate(
        recipe_cnt=Count('recipe__id'))
    page, paginator = paginator_mixin(request, authors)
    return render(request, 'myFollow.html',
                  {'page': page, 'paginator': paginator})


def purchases(request):
    recipes = Recipe.objects.filter(recipe_purchase__author=request.user)
    return render(request, 'shopList.html', {'recipes': recipes})


def purchase_remove(request, recipe_id):
    purchase = Purchase.objects.get(author=request.user, recipe__id=recipe_id)
    if request.user == purchase.author:
        purchase.delete()
        return redirect('purchases')
    return redirect('index')


def purchase_count(request):
    if request.user.is_authenticated:
        return {'purchase_count': Purchase.objects.filter(author=request.user).count()}
    else:
        return {'purchase_count': None}


@login_required
def get_shoplist(request):
    ingredients = Recipe.objects.prefetch_related('ingredients', 'recipe_cnt'
                                                  ).filter(recipe_purchase__author=request.user
                                                           ).order_by('ingredients__name').values(
        'ingredients__name', 'ingredients__measure_unit'
    ).annotate(
        cnt=Sum('recipe_cnt__cnt'))
    ingredient_txt = [
        (f"\u2022 {item['ingredients__name'].capitalize()} "
         f"({item['ingredients__measure_unit']}) \u2014 {item['cnt']} \n")
        for item in ingredients
    ]
    filename = 'shoplist.txt'
    response = HttpResponse(ingredient_txt, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
