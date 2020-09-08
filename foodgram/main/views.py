from django.shortcuts import render
from main.models import Amount, Subscription, Ingredient, Recipe, User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect


def index(request):
    recipe_list = Recipe.objects.select_related(
        'author').order_by('-pub_date')

    paginator = Paginator(recipe_list, 5)
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
    recipes_profile = Recipe.objects.filter(
                                        author=profile).order_by("-pub_date")

    paginator = Paginator(recipes_profile, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    if request.user.is_authenticated:
        if Subscription.objects.filter(user=request.user, author=profile).count():
            following = True
    if request.user != profile:
        follow_button = True

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
    context = {}

    if request.user.is_authenticated:
        return render(request, 'singlePage.html', context)
    # elif автор

    return render(request, 'singlePageNotAuth.html', context)


def recipe_edit(request, username, recipe_id):
    context = {}
    return render(request, "formChangeRecipe.html", context)


def favorites(request):
    context = {}
    return render(request, "favorite.html", context)


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
    
    subscriptions = Subscription.objects.filter(user=request.user).values('author')

    recipes_list = Recipe.objects.filter(author__in=subscriptions).order_by("-pub_date")

    paginator = Paginator(recipes_list, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'myFollow.html', {
        'paginator': paginator,
        'page': page
    }
    )