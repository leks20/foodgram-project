from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new', views.new_recipe, name="new_recipe"),
    path("favorites", views.favorites, name="favorites"),
    path("ingredients", views.ingredients, name="ingredients"),
    path("change_favorites/<recipe_id>", views.change_favorites, name="change_favorites"),
    path("follow", views.my_follow, name="my_follow"),
    path("shop_list", views.shop_list, name="shop_list"),
    path("purchases", views.get_purchases, name="get_purchases"),
    path("purchases/<recipe_id>", views.purchases, name="purchases"),
    path("subscriptions/<author_id>", views.subscriptions, name="subscriptions"),
    path("<username>", views.profile, name="profile"),
    path("<username>/<recipe_id>", views.recipe_view, name="recipe"),
    path("<username>/<recipe_id>/edit", views.recipe_edit, name="recipe_edit"),
    path("<username>/<recipe_id>/delete", views.recipe_delete, name="recipe_delete")

]
