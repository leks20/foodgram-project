from django.contrib import admin

from .models import (Amount, Favorite, Ingredient, Recipe, ShopList,
                     Subscription, Tag, User)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'show_favorites')
    list_filter = ('author', 'title', 'tags',)

    def show_favorites(self, obj):
        result = Favorite.objects.filter(recipe=obj).count()
        return result

    show_favorites.short_description = "Favorite"


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit',)
    list_filter = ('title',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'first_name',)


@admin.register(Amount)
class AmountAdmin(admin.ModelAdmin):
    pass


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following')


@admin.register(ShopList)
class ShopListAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'style', 'human_name')
