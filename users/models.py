from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Информация про пользователя"""
    user_weight = models.FloatField(default=0)
    user_purpose = models.BooleanField(default=0)
    calories_limit = models.IntegerField(default=0)
    proteins_limit = models.IntegerField(default=0)
    fats_limit = models.IntegerField(default=0)
    carbohydrates_limit = models.IntegerField(default=0)

    def __str__(self):
        return self.username
