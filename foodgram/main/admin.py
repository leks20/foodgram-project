from django.contrib import admin

from .models import (Amount, Favorite, Follow, Ingredient, Recipe,
                     ShoppingList, User)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'show_favorite_number')
    list_filter = ('author', 'title', 'tag',)

    def show_favorite_number(self, obj):
        result = Favorite.objects.filter(recipe=obj).count()
        return result

    show_favorite_number.short_description = "Favorite"

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
class AmountAdmin(admin.ModelAdmin):
    pass


@admin.register(Follow)
class AmountAdmin(admin.ModelAdmin):
    pass


@admin.register(ShoppingList)
class AmountAdmin(admin.ModelAdmin):
    pass
