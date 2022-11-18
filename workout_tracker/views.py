import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView

from .forms import ExerciseForm
from .models import *


class ExerciseList(LoginRequiredMixin, ListView):
    """Главная страница со списком доступных блюд"""
    model = Exercise
    template_name = 'workout_tracker/exercise_list.html'
    login_url = '/login/'
    paginate_by = 8
    context_object_name = 'exercises'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список пражнений'
        return context

    def get_queryset(self):
        return Exercise.objects.filter(Q(creator=self.request.user.id) | Q(creator=None))


@login_required
def add_exercise(request):
    """Страница с добавлением нового блюда в БД"""

    if request.method == 'POST':
        exercise_form = ExerciseForm(request.POST, request.FILES)
        if exercise_form.is_valid():
            new_exercise = exercise_form.save(commit=False)
            new_exercise.creator = request.user
            new_exercise.save()
            print(exercise_form.cleaned_data)
            muscle_groups = exercise_form.cleaned_data['muscle_groups']
            for muscle_group in muscle_groups:
                new_exercise.muscle_groups.add(muscle_group)
            new_exercise.save()
            return render(request, 'workout_tracker/add_exercise.html', {
                'exercise_form': ExerciseForm(),
                'success': True
            })
        else:
            return render(request, 'workout_tracker/add_exercise.html',
                          {'exercise_form': ExerciseForm()})
    else:
        return render(request, 'workout_tracker/add_exercise.html',
                      {'exercise_form': ExerciseForm()})


class TodayWorkout(LoginRequiredMixin, ListView):
    model = Workout
    template_name = 'workout_tracker/today_workout.html'
    context_object_name = 'workouts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Тренировки за сегодня'
        return context

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user.id,
                                      time=datetime.date.today())


@login_required
def workout_details(request, workout_id):
    if request.method == 'POST':
        try:
            exercise = request.POST['exercise']
            weight = request.POST['weight']
            reps = request.POST['reps']
            exercise = Exercise.objects.get(name=exercise)
            muscle_groups = exercise.muscle_groups.all()
            workout = Workout.objects.get(id=workout_id)
            for muscle_group in muscle_groups:
                workout.muscle_groups.add(muscle_group)
            workout.save()
            new_set = Set(exercise=exercise, workout=workout,
                          weight=weight, reps=reps)
            new_set.save()

            workout = Workout.objects.filter(id=workout_id).first()
            sets = Set.objects.filter(workout=workout)
            sets_count = len(sets)
            exercises_dct = {}
            for set in sets:
                exercises_dct[set.exercise] = []
            for set in sets:
                exercises_dct[set.exercise].append(set)
            exercises = Exercise.objects.filter(
                Q(creator=request.user.id) | Q(creator=None))
            return render(request,
                          'workout_tracker/today_workout_details.html', {
                              'exercises_dct': exercises_dct,
                              'title': 'Тренировка',
                              'workout_id': workout_id,
                              'exercises': exercises,
                              'last_exercise': exercise.name,
                              'last_weight': weight,
                              'last_reps': reps,
                              'sets_count': sets_count
                          })
        except:
            workout = Workout.objects.filter(id=workout_id).first()
            sets = Set.objects.filter(workout=workout)
            sets_count = len(sets)
            exercises_dct = {}
            for set in sets:
                exercises_dct[set.exercise] = []
            for set in sets:
                exercises_dct[set.exercise].append(set)
            exercises = Exercise.objects.filter(
                Q(creator=request.user.id) | Q(creator=None))
            return render(request,
                          'workout_tracker/today_workout_details.html',
                          {
                              'exercises_dct': exercises_dct,
                              'title': 'Тренировка',
                              'workout_id': workout_id,
                              'exercises': exercises,
                              'form_error': True,
                              'sets_count': sets_count
                          })
    else:
        workout = Workout.objects.filter(id=workout_id).first()
        sets = Set.objects.filter(workout=workout)
        sets_count = len(sets)
        exercises_dct = {}
        for set in sets:
            exercises_dct[set.exercise] = []
        for set in sets:
            exercises_dct[set.exercise].append(set)
        exercises = Exercise.objects.filter(
            Q(creator=request.user.id) | Q(creator=None))
        return render(request, 'workout_tracker/today_workout_details.html', {
            'exercises_dct': exercises_dct,
            'title': 'Тренировка',
            'workout_id': workout_id,
            'exercises': exercises,
            'sets_count': sets_count
        })


@login_required
def workout_delete_set(request, workout_id, set_id, exercise_id):
    workout = Workout.objects.get(id=workout_id)
    del_set = Set.objects.get(id=set_id)
    del_set_muscle_groups = [str(group) for group in del_set.exercise.muscle_groups.all()]
    print(del_set_muscle_groups)
    del_set.delete()
    sets = Set.objects.filter(workout_id=workout_id)
    workout_muscle_groups = []
    for set in sets:
        for group in set.exercise.muscle_groups.all():
            workout_muscle_groups.append(str(group))
    for group in del_set_muscle_groups:
        if group not in workout_muscle_groups:
            workout.muscle_groups.remove(MuscleGroup.objects.get(name=group))
            workout.save()
    return HttpResponseRedirect(f'/workout-tracker/today_workout/{workout_id}/#{exercise_id}')


@login_required
def update_set(request, workout_id, set_id):
    set = Set.objects.get(id=set_id)
    weight = request.POST['weight']
    reps = request.POST['reps']
    set.weight = weight
    set.reps = reps
    set.save()
    return HttpResponseRedirect(f'/workout-tracker/today_workout/{workout_id}/')


@login_required
def add_workout(request):
    new_workout = Workout.objects.create(user=request.user, time=datetime.date.today())
    return HttpResponseRedirect(f'/workout-tracker/today_workout/{new_workout.id}/')


@login_required
def delete_workout(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    workout.delete()
    return HttpResponseRedirect(f'/workout-tracker/today_workout/')
