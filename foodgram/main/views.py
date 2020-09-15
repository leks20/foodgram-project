from django.shortcuts import render
from .models import Amount, Favorite, ShopList, Subscription, Tag, Ingredient, Recipe, User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
import json
from django.http import JsonResponse
from .forms import RecipeCreateForm
from .utils import get_ingredients, get_tags_for_edit


def index(request):
    tags_list = request.GET.getlist('filters')

    recipe_list = Recipe.objects.filter(tags__value__in=tags_list).select_related(
        'author').order_by('-pub_date').prefetch_related('tags').distinct()

    all_tags = Tag.objects.all()

    shop_list_ids = [id[0] for id in list(ShopList.objects.values_list('recipe_id'))]
    favorites_ids = [id[0] for id in list(Favorite.objects.values_list('recipe_id'))]

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    if request.user.is_authenticated:
        shop_list_count = ShopList.objects.filter(user=request.user).count()

        return render(request, 'indexAuth.html', {
            'paginator': paginator,
            'page': page,
            'shop_list_ids': shop_list_ids,
            'favorites_ids': favorites_ids,
            'shop_list_count': shop_list_count,
            'all_tags': all_tags,
            'tags_list': tags_list,
        }
        )

    return render(request, 'indexNotAuth.html', {
        'paginator': paginator,
        'page': page,
        'shop_list_ids': shop_list_ids,
        'all_tags': all_tags,
        'tags_list': tags_list,

    }
    )


def profile(request, username):
    follower = False
    follow_button = False

    tags_list = request.GET.getlist('filters')
    all_tags = Tag.objects.all()

    profile = get_object_or_404(User, username=username)
    recipes_profile = Recipe.objects.filter(author=profile).filter(
        tags__value__in=tags_list).select_related('author').order_by("-pub_date").distinct()

    favorites_ids = [id[0] for id in list(Favorite.objects.values_list('recipe_id'))]

    if request.user.is_authenticated:
        shop_list_count = ShopList.objects.filter(user=request.user).count()
    else:
        shop_list_count = None

    if request.user.is_authenticated and request.user != profile:
        follow_button = True

        if Subscription.objects.filter(user=request.user, author=profile).exists():
            follower = True

    paginator = Paginator(recipes_profile, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "authorRecipe.html", {
        'paginator': paginator,
        'page': page,
        'profile': profile,
        'follower': follower,
        'follow_button': follow_button,
        'favorites_ids': favorites_ids,
        'shop_list_count': shop_list_count,
        'all_tags': all_tags,
        'tags_list': tags_list,
        }
        )


def recipe_view(request, username, recipe_id):
    owner = False
    follower = False
    in_shop_list = False

    recipe = Recipe.objects.select_related('author').get(pk=recipe_id)
    favorites_ids = [id[0] for id in list(Favorite.objects.values_list('recipe_id'))]

    if not request.user.is_authenticated:
        return render(request, 'singlePageNotAuth.html', {'recipe': recipe})

    shop_list_count = ShopList.objects.filter(user=request.user).count()

    if request.user.username == recipe.author.username:
        owner = True

    if Subscription.objects.filter(user=request.user, author=recipe.author).exists():
        follower = True

    if ShopList.objects.filter(recipe=recipe).exists():
        in_shop_list = True

    return render(request, 'singlePage.html', {
        'recipe': recipe,
        'owner': owner,
        'follower': follower,
        'in_shop_list': in_shop_list,
        'favorites_ids': favorites_ids,
        'shop_list_count': shop_list_count,
        })


# функция для подсказки при написании ингредиента в форме создания рецепта
# возвращает JSON с ингредиентами по первым введенным буквам
def ingredients(request):
    text = request.GET['query']
    ingredients = Ingredient.objects.filter(title__startswith=text)

    ing_list = []

    for ing in ingredients:
        ing_dict = {}
        ing_dict['title'] = ing.title
        ing_dict['dimension'] = ing.dimension
        ing_list.append(ing_dict)

    return JsonResponse(ing_list, safe=False)


def new_recipe(request):
    shop_list_count = ShopList.objects.filter(user=request.user).count()

    if request.method == "POST":
        form = RecipeCreateForm(request.POST or None, files=request.FILES or None)

        if form.is_valid():

            my_recipe = form.save(commit=False)
            my_recipe.author = request.user
            my_recipe.save()

            ingredients = get_ingredients(request)

            for title, quantity in ingredients.items():
                ingredient = Ingredient.objects.get(title=title)
                amount = Amount(recipe=my_recipe, ingredient=ingredient, quantity=quantity)
                amount.save()
            
            form.save_m2m()
            return redirect('recipe', recipe_id=my_recipe.id, username=request.user.username)

    form = RecipeCreateForm()
    return render(request, "formRecipe.html", {
        'shop_list_count': shop_list_count,
        'form': form,
    })


@login_required
def recipe_edit(request, username, recipe_id):
    shop_list_count = ShopList.objects.filter(user=request.user).count()

    recipe = get_object_or_404(Recipe, pk=recipe_id)
    author = get_object_or_404(User, id=recipe.author_id)
    all_tags = recipe.tags.values_list('value', flat=True)

    if request.user != author:
        return redirect("recipe", username=username, recipe_id=recipe_id)
    
    if request.method == 'POST':
        recipe_tags = get_tags_for_edit(request) # [QuerySet, QuerySet...]
        recipe_ingredients = get_ingredients(request) # {...}

        form = RecipeCreateForm(request.POST, files=request.FILES or None, instance=recipe)
        print(form.errors)

        if form.is_valid():
            print('VALID')

            # new_recipe = form.save(commit=False)
            # new_recipe.pub_date_at = dt.datetime.today()
            # new_recipe.ingredients = recipe_data.get('ingredients')
            # new_recipe.save()
            # new_recipe.tags.set(recipe_data.get('tags'))
            # return redirect('recipe_item', recipe_id=recipe_id)           
            
            my_recipe = form.save(commit=False)
            for title, quantity in recipe_ingredients.items():
                ingredient = Ingredient.objects.get(title=title)
                amount = Amount(recipe=my_recipe, ingredient=ingredient, quantity=quantity)
                amount.save()
            my_recipe.tags.set(recipe_tags)
            my_recipe.save()

            return redirect('recipe', recipe_id=recipe.id, username=request.user.username)




    form = RecipeCreateForm(instance=recipe)
    return render(request, "formChangeRecipe.html", {
        'shop_list_count': shop_list_count,
        'form': form,
        'recipe': recipe,
        'all_tags': all_tags,
    })


@login_required
def recipe_delete(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    author = get_object_or_404(User, id=recipe.author_id)

    if request.user != author:
        return redirect("recipe", username=username, recipe_id=recipe_id)
    
    recipe.delete()
    return redirect("profile", username=username)


@login_required
def favorites(request):
    tags_list = request.GET.getlist('filters')
    all_tags = Tag.objects.all()

    favorite_ids = Favorite.objects.filter(user=request.user).values('recipe_id')
    recipe_list = Recipe.objects.filter(id__in=favorite_ids).filter(tags__value__in=tags_list).distinct()

    shop_list_ids = [id[0] for id in list(ShopList.objects.values_list('recipe_id'))]
    favorites_ids = [id[0] for id in list(Favorite.objects.values_list('recipe_id'))]
    shop_list_count = ShopList.objects.filter(user=request.user).count()

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "favorites.html", {
        'paginator': paginator,
        'page': page,
        'shop_list_ids': shop_list_ids,
        'favorites_ids': favorites_ids,
        'shop_list_count': shop_list_count,
        'all_tags': all_tags,
        'tags_list': tags_list,
    }
    )


@login_required
def change_favorites(request, recipe_id):

    # добавить в избранное
    if request.method == "POST":
        recipe_id = json.loads(request.body).get('id')
        recipe = Recipe.objects.get(pk=recipe_id)

        if Favorite.objects.filter(recipe=recipe).exists():
            return JsonResponse({'success': 'false'})

        Favorite.objects.create(user=request.user, recipe=recipe)
        return JsonResponse({'success': 'true'})

    # удалить из изобранного
    elif request.method == "DELETE":
        recipe = Recipe.objects.get(pk=recipe_id)

        removed = Favorite.objects.filter(user=request.user, recipe=recipe).delete()

        if removed:
            return JsonResponse({'success': 'true'})

        return JsonResponse({'success': 'false'})


# отображение страницы со списком покупок
@login_required
def shop_list(request):
    if request.GET:
        recipe_id = request.GET.get('recipe_id')
        ShopList.objects.get(recipe__id=recipe_id).delete()

    shop_list_ids = ShopList.objects.filter(user=request.user).values_list('recipe_id')
    shop_list_count = ShopList.objects.filter(user=request.user).count()

    purchases = Recipe.objects.filter(id__in=shop_list_ids)

    return render(request, "shopList.html", {
        'purchases': purchases,
        'shop_list_count': shop_list_count
    }
    )


# скачать лист покупок
@login_required
def get_purchases(request):
    # получаем список рецептов, находящихся в ShopList 
    recipes = Recipe.objects.filter(id__in=ShopList.objects.values_list('recipe_id', flat=True))
    
    
    
    
    
    with open('shop_list.txt', w) as file:

    return None


@login_required
def purchases(request, recipe_id):

    # добавить в список покупок
    if request.method == "POST":
        recipe_id = json.loads(request.body).get('id')
        recipe = Recipe.objects.get(pk=recipe_id)

        if ShopList.objects.filter(recipe=recipe).exists():
            return JsonResponse({'success': 'false'})

        ShopList.objects.create(user=request.user, recipe=recipe)
        return JsonResponse({'success': 'true'})

    # удалить из списка покупок
    elif request.method == "DELETE":
        recipe = Recipe.objects.get(pk=recipe_id)

        removed = ShopList.objects.filter(user=request.user, recipe=recipe).delete()

        if removed:
            return JsonResponse({'success': 'true'})

        return JsonResponse({'success': 'false'})


@login_required
def subscriptions(request, author_id):
    
    # подписаться на автора
    if request.method == "POST":
        author_id = json.loads(request.body).get('id')
        author = get_object_or_404(User, id=author_id)

        if request.user == author or Subscription.objects.filter(user=request.user, author=author).exists():
            return JsonResponse({'success': 'false'})

        Subscription.objects.create(user=request.user, author=author)
        return JsonResponse({'success': 'true'})

    # отписаться от автора
    elif request.method == "DELETE":
        author = get_object_or_404(User, id=author_id)

        removed = Subscription.objects.filter(user=request.user, author=author).delete()

        if removed:
            return JsonResponse({'success': 'true'})

        return JsonResponse({'success': 'false'})


@login_required
def my_follow(request):

    subscription_ids = Subscription.objects.filter(user=request.user).values('author_id')
    subscriptions = User.objects.filter(id__in=subscription_ids).annotate(recipe_count=Count('recipes'))
    shop_list_count = ShopList.objects.filter(user=request.user).count()

    recipe_dict = {}
    for sub in subscriptions:
        recipe_dict[sub] = Recipe.objects.filter(author=sub).order_by('-pub_date')[:3]

    paginator = Paginator(subscriptions, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'myFollow.html', {
        'paginator': paginator,
        'page': page,
        'recipe_dict': recipe_dict,
        'shop_list_count': shop_list_count
    }
    )