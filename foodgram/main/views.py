from django.shortcuts import render
from main.models import Amount, Favorite, Subscription, Ingredient, Recipe, User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count


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


def new_recipe(request):
    context = {}
    return render(request, "formRecipe.html", context)


def recipe_view(request, username, recipe_id):

    recipe = Recipe.objects.select_related('author').get(pk=recipe_id)
    author = False

    if not request.user.is_authenticated:
        return render(request, 'singlePageNotAuth.html', {'recipe': recipe})

    if request.user.username == recipe.author.username:
        author = True

    return render(request, 'singlePage.html', {'recipe': recipe, 'author': author})


def recipe_edit(request, username, recipe_id):
    context = {}
    return render(request, "formChangeRecipe.html", context)


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


def purchases(request):
    context = {}
    return render(request, "shopList.html", context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user == author or Subscription.objects.filter(
            user=request.user, author=author).exists():
        return redirect("profile", username=username)
    else:
        Subscription.objects.create(user=request.user, author=author)
        return redirect("profile", username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user == author:
        return redirect("profile", username=username)
    else:
        following = Subscription.objects.get(user=request.user, author=author)
        following.delete()
        return redirect("profile", username=username)


def subscriptions(request):

    subscription_ids = Subscription.objects.filter(user=request.user).values('author_id')
    subscriptions = User.objects.filter(id__in=subscription_ids).annotate(recipe_count=Count('recipes'))

    recipe_dict = {}
    for sub in subscriptions:
        recipe_dict[sub] = Recipe.objects.filter(author=i)

    paginator = Paginator(subscriptions, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'myFollow.html', {
        'paginator': paginator,
        'page': page,
        'recipe_dict': recipe_dict
    }
    )