from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_recipe, name="new_recipe"),
    path("favorite/", views.favorite, name="favorite"),
    path("following/", views.profile_following, name="profile_following"),
    path("purchases/", views.purchases, name="purchases"),
    path("<username>/", views.profile, name="profile"),
    path("<username>/follow/", views.profile_follow, name="profile_follow"),
    path("<username>/unfollow/", views.profile_unfollow, name="profile_unfollow"),
    path("<username>/<recipe_id>/", views.recipe_view, name="recipe"),
    path("<username>/<recipe_id>/edit/", views.recipe_edit, name="recipe_edit")
]
