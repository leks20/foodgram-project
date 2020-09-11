from django.shortcuts import render
from main.models import Amount, Favorite, ShopList, Subscription, Ingredient, Recipe, User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
import json
from django.http import JsonResponse


def index(request):
    recipe_list = Recipe.objects.select_related(
        'author').order_by('-pub_date').prefetch_related('tags')

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    if request.user.is_authenticated:
        return render(request, 'indexAuth.html', {
            'paginator': paginator,
            'page': page
        }
        )

    return render(request, 'indexNotAuth.html', {
        'paginator': paginator,
        'page': page
    }
    )


def profile(request, username):
    following = False
    follow_button = False

    profile = get_object_or_404(User, username=username)
    recipes_profile = (Recipe.objects.filter(author=profile).select_related('author').order_by("-pub_date"))

    if request.user.is_authenticated and request.user != profile:
        follow_button = True

        if Subscription.objects.filter(user=request.user, author=profile).exists():
            following = True

    paginator = Paginator(recipes_profile, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "authorRecipe.html", {
        'paginator': paginator,
        'page': page,
        'profile': profile,
        'following': following,
        'follow_button': follow_button,
        }
        )


def recipe_view(request, username, recipe_id):
    author = False
    # follower = False

    recipe = Recipe.objects.select_related('author').get(pk=recipe_id)

    if not request.user.is_authenticated:
        return render(request, 'singlePageNotAuth.html', {'recipe': recipe})

    if request.user.username == recipe.author.username:
        author = True

    # if Subscription.objects.filter(user=request.user, author=author).exists():
    #     follower = True

    return render(request, 'singlePage.html', {
        'recipe': recipe,
        'author': author,
        # 'follower': follower,
        })


def new_recipe(request):
    context = {}
    return render(request, "formRecipe.html", context)


def recipe_edit(request, username, recipe_id):
    context = {}
    return render(request, "formChangeRecipe.html", context)


@login_required
def favorites(request):
    favorite_ids = Favorite.objects.filter(user=request.user).values('recipe_id')
    recipe_list = Recipe.objects.filter(id__in=favorite_ids)

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "favorites.html", {
        'recipe_list': recipe_list,
        'paginator': paginator,
        'page': page
    }
    )


@login_required
def purchases(request):

    shop_list_ids = ShopList.objects.filter(user=request.user).values_list('recipe_id')
    shop_list_count = ShopList.objects.filter(user=request.user).count()

    purchases = Recipe.objects.filter(id__in=shop_list_ids)

    return render(request, "shopList.html", {
        'purchases': purchases,
        'shop_list_count': shop_list_count
    }
    )


@login_required
def subscriptions(request, author_id=None):
    import pdb; pdb.set_trace()

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

    recipe_dict = {}
    for sub in subscriptions:
        recipe_dict[sub] = Recipe.objects.filter(author=sub).order_by('-pub_date')[:3]

    paginator = Paginator(subscriptions, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'myFollow.html', {
        'paginator': paginator,
        'page': page,
        'recipe_dict': recipe_dict
    }
    )