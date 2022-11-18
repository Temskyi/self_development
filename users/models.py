from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Информация про пользователя"""
    GAIN = "G"
    LOSS = "L"
    PURPOSES = [
        (GAIN, "Набор веса"),
        (LOSS, "Похудение"),
    ]
    user_purpose = models.CharField(
        max_length=1,
        choices=PURPOSES,
        default=GAIN
    )
    user_weight = models.FloatField(default=0)
    calories_limit = models.IntegerField(default=0)
    proteins_limit = models.IntegerField(default=0)
    fats_limit = models.IntegerField(default=0)
    carbohydrates_limit = models.IntegerField(default=0)

    def __str__(self):
        return self.username
