from django.urls import path

from .views import *

urlpatterns = [
    path('', TodayWorkout.as_view(), name='workout_tracker_index'),
    path('exercise_list/', ExerciseList.as_view(), name='exercise_list'),

    path('add_exercise/', add_exercise, name='add_exercise'),

    path('today_workout/', TodayWorkout.as_view(), name='today_workout'),
    path('today_workout/<int:workout_id>/', workout_details, name='today_workout_details'),
    path('today_workout/add_workout/', add_workout, name='add_workout'),
    path('today_workout/delete_workout/<int:workout_id>/', delete_workout, name='delete_workout'),
    path('today_workout/<int:workout_id>/set_delete/<int:set_id>/<int:exercise_id>/', workout_delete_set, name='delete_set'),
    path('today_workout/<int:workout_id>/set_update/<int:set_id>/<int:exercise_id>/', update_set, name='update_set'),

    path('workout_history/', workout_history, name='workout_history')
]
