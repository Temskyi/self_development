from django.db import models
from django.conf import settings


class Dish(models.Model):
    """Категории блюд"""
    name = models.CharField(max_length=100, db_index=True,
                            verbose_name='Название блюда')
    calories = models.IntegerField(verbose_name='Калории')
    protein = models.DecimalField(max_digits=4, decimal_places=2,
                                  verbose_name='Белки')
    fat = models.DecimalField(max_digits=4, decimal_places=2,
                              verbose_name='Жиры')
    carbohydrates = models.DecimalField(max_digits=4, decimal_places=2,
                                        verbose_name='Углеводы')
    image = models.ImageField(upload_to='calorie_tracker/photos/', blank=True,
                              null=True, verbose_name='Фото')
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
        ordering = ['id']


class Day(models.Model):
    total_calories = models.IntegerField(verbose_name='Калории', default=0)
    total_protein = models.DecimalField(max_digits=7, decimal_places=2,
                                        default=0.00)
    total_fat = models.DecimalField(max_digits=7, decimal_places=2,
                                    default=0.00)
    total_carbohydrates = models.DecimalField(max_digits=7, decimal_places=2,
                                              default=0.00)
    day = models.DateField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.day)

    class Meta:
        verbose_name = "День"
        verbose_name_plural = "Дни"
        ordering = ['id']


class Meal(models.Model):
    """Приёмы пищи"""
    total_calories = models.IntegerField(verbose_name='Калории', default=0)
    total_protein = models.DecimalField(max_digits=7, decimal_places=2,
                                        default=0.00)
    total_fat = models.DecimalField(max_digits=7, decimal_places=2,
                                    default=0.00)
    total_carbohydrates = models.DecimalField(max_digits=7, decimal_places=2,
                                              default=0.00)
    meal_time_create = models.DateTimeField(auto_now_add=True,
                                            verbose_name="Время создания")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    day = models.ForeignKey(
        Day,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.meal_time_create)

    class Meta:
        verbose_name = "Приём пищи"
        verbose_name_plural = "Приёмы пищи"
        ordering = ['id']


class Product(models.Model):
    """Продукты, из которых состоят приёмы пищи"""
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
    )
    meal = models.ForeignKey(
        Meal,
        on_delete=models.CASCADE,
    )
    weight = models.IntegerField()
    calories = models.IntegerField(verbose_name='Калории')
    protein = models.DecimalField(max_digits=5, decimal_places=2)
    fat = models.DecimalField(max_digits=5, decimal_places=2)
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.dish.name + self.weight

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['id']


class Weight(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    weight = models.DecimalField(max_digits=7, decimal_places=2)
    entry_date = models.DateField()

    class Meta:
        verbose_name = 'Вес'
        verbose_name_plural = 'Вес'

    def __str__(self):
        return f'{self.user.username} - {self.weight} kg on {self.entry_date}'

