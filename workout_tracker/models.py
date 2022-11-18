from django.conf import settings
from django.db import models


class MuscleGroup(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Группа мышц"
        verbose_name_plural = "Группы мышц"
        ordering = ['id']


class Exercise(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='workout_tracker/photos/', blank=True,
                              null=True, verbose_name='Фото')
    muscle_groups = models.ManyToManyField(MuscleGroup,
                                           verbose_name="Группы мышц")
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
        verbose_name = "Упражнение"
        verbose_name_plural = "Упражнения"
        ordering = ['id']


class Workout(models.Model):
    time = models.DateField(auto_now_add=True,
                            verbose_name="День тренировки")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True
    )
    muscle_groups = models.ManyToManyField(MuscleGroup,
                                           verbose_name="Группы мышц",
                                           default=None,
                                           blank=True,
                                           null=True)

    def __str__(self):
        return str(self.time)

    class Meta:
        verbose_name = "Тренировка"
        verbose_name_plural = "Тренировки"
        ordering = ['id']


class Set(models.Model):
    exercise = models.ForeignKey(Exercise,
                                 on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout,
                                on_delete=models.CASCADE)
    weight = models.FloatField(verbose_name="Вес")
    reps = models.IntegerField(verbose_name="Повторения")

    def __str__(self):
        return f"{self.exercise} {self.weight}Кг на {self.reps} повт."

    class Meta:
        verbose_name = "Подход"
        verbose_name_plural = "Подходы"
        ordering = ['id']

    def get_int_weight(self):
        return int(self.weight)

    def get_weight(self):
        if self.weight % 1 == 0:
            return int(self.weight)
        return self.weight
