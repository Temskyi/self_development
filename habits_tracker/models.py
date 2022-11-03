from django.db import models
from django.contrib.auth.models import User


class Habits(models.Model):
    """Категории привычек"""
    name = models.CharField(max_length=100, db_index=True)
    qr = models.ImageField(upload_to="qr_images")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"


class Tracking(models.Model):
    """Привычки за день"""
    habit = models.ForeignKey(
        "Habits",
        on_delete=models.CASCADE,
    )
    is_completed = models.BooleanField('Завершено', default=False)
    day = models.DateField()

    def __str__(self):
        return self.habit.name + " " + str(self.day)

    class Meta:
        verbose_name = "Трэкинг"
        verbose_name_plural = "Трэкинг"
        ordering = ['day']


