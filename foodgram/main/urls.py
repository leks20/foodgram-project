from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new', views.new_recipe, name="new_recipe"),
    path("favorites", views.favorites, name="favorites"),
    path("follow", views.my_follow, name="my_follow"),
    path("purchases", views.purchases, name="purchases"),
    path("subscriptions/<author_id>", views.subscriptions, name="subscriptions"),
    path("<username>", views.profile, name="profile"),
    path("<username>/<recipe_id>", views.recipe_view, name="recipe"),
    path("<username>/<recipe_id>/edit", views.recipe_edit, name="recipe_edit")
]
