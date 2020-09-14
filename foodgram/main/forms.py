from django.forms import ModelForm
from django import forms
from main.models import Recipe


class RecipeCreateForm(ModelForm):

    class Meta:
        model = Recipe
        fields = ('title', 'tags', "time", "description", "image",)
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
