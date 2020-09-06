from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
]
