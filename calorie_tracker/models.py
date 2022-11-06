from django.db import models
from django.conf import settings


class Dish(models.Model):
    """Категории блюд"""
    name = models.CharField(max_length=100, db_index=True, verbose_name='Название блюда')
    calories = models.IntegerField(verbose_name='Калории')
    protein = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Белки')
    fat = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Жиры')
    carbohydrates = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Углеводы')
    image = models.ImageField(upload_to='calorie_tracker/photos/', blank=True, null=True, verbose_name='Фото')
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"


class Product(models.Model):
    """Продукты, из которых состоят приёмы пищи"""
    dish_id = models.ForeignKey(
        "Dish",
        on_delete=models.CASCADE,
    )
    meal_id = models.ForeignKey(
        "meal",
        on_delete=models.CASCADE,
    )
    weight = models.IntegerField()
    protein = models.DecimalField(max_digits=5, decimal_places=2)
    fat = models.DecimalField(max_digits=5, decimal_places=2)
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.dish_id.name + self.weight

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Meal(models.Model):
    """Приёмы пищи"""
    total_calories = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    total_protein = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    total_fat = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    total_carbohydrates = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    meal_time = models.DateTimeField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user.name + self.meal_time

    class Meta:
        verbose_name = "Приём пищи"
        verbose_name_plural = "Приёмы пищи"



