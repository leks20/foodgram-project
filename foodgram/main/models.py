from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    class Role(models.TextChoices):
        ANONYM = 'anonym', _('Anonym')
        USER = 'user', _('User')
        ADMIN = 'admin', _('Admin')

    email = models.EmailField(_('email address'), blank=False, unique=True)
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
        )
    confirmation_code = models.CharField(max_length=100, blank=True, )

    def __str__(self):
        return self.username


class Tag(models.Model):
    MEALTIME = [
        ('1', 'Breakfast'),
        ('2', 'Lunch'),
        ('3', 'Dinner'),
    ]
    name = models.CharField(max_length=50, choices=MEALTIME)


class Ingredient(models.Model):
    title = models.CharField(max_length=200)  # choice = ...
    unit = models.CharField(max_length=50)  # choice = ...

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes'
    )
    pub_date = models.DateTimeField(
        "Дата публикации",
        auto_now_add=True,
        db_index=True
    )
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='main/', null=True, blank=True)
    description = models.TextField()
    tag = models.ManyToManyField(Tag)
    ingredients = models.ManyToManyField(Ingredient, through='Amount')
    time = models.DurationField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Amount(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipes'
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='ingredients'
    )
    quantity = models.DecimalField(max_digits=5, decimal_places=2)


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorite_recipes',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites"
    )


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following"
    )


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shopping_list"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shopping_list'
    )

