from django.contrib import admin
from .models import MuscleGroup, Exercise, Workout, Set

admin.site.register(MuscleGroup)
admin.site.register(Exercise)
admin.site.register(Workout)
admin.site.register(Set)
