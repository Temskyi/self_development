import os
import qrcode
import datetime
from pathlib import Path
from calendar import monthrange

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect

from .models import *
from django.conf.global_settings import ALLOWED_HOSTS


def _get_days_in_month(num=0, year=0):
    num = int(num)
    year = datetime.datetime.now().year - year
    month = datetime.datetime.now().month - num
    if month < 1:
        year -= 1
        month += 12
    days_in_month = monthrange(year,
                               month)[1]
    return days_in_month


def _get_today_habits(user_id):
    """Получение привычек на день"""
    user_habits = Habits.objects.filter(user=user_id)
    today_habits = Tracking.objects.filter(day=datetime.date.today(),
                                           habit__in=user_habits).select_related('habit').order_by('id')

    if len(today_habits) == 0:
        objects_list = []
        for d in range(1, _get_days_in_month() + 1):
            for habit in Habits.objects.filter(user=user_id):
                day = f'{datetime.datetime.now().year}-{datetime.datetime.now().month}-{d}'
                objects_list.append(Tracking(habit=habit, day=day))
        Tracking.objects.bulk_create(objects_list)

        today_habits = Tracking.objects.filter(day=datetime.date.today(),
                                               habit__in=user_habits).order_by('id')

    return today_habits


class HabitsHome(LoginRequiredMixin, ListView):
    """Класс представления главной страницы с привычками на сегодня"""
    model = Tracking
    template_name = 'habits/index.html'
    login_url = '/login/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today_habits'] = _get_today_habits(self.request.user.id)
        context['title'] = ''
        return context


class Statistic(LoginRequiredMixin, ListView):
    """Страница со статистикой привычек за месяц"""
    model = Tracking
    template_name = 'habits/statistic.html'
    login_url = '/login/'

    months = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль',
              'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']

    @classmethod
    def get_previous_month_date(cls, num):
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month - num
        if month < 1:
            year -= 1
            month += 12
        if len(str(month)) == 1:
            month = "0" + str(month)
        return f"{year}-{month}-01"

    @classmethod
    def get_month_name(cls, num):
        num = int(num)
        while num < 1:
            num += 12
        return cls.months[num - 1]

    @classmethod
    def get_month_number(cls, num=0):
        month = datetime.datetime.now().month
        month_number = month - num
        while month_number < 1:
            month_number += 12
        if len(str(month_number)) == 1:
            month_number = "0" + str(month_number)
        return month_number

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_habits = Habits.objects.filter(user=self.request.user.id)

        completed_months = []
        month_before_previous = self.get_month_name(
            datetime.datetime.now().month - 2)
        if Tracking.objects.filter(
                day=self.get_previous_month_date(2),
                habit__in=user_habits).first():
            completed_months.append(month_before_previous)
        previous_month = self.get_month_name(datetime.datetime.now().month - 1)
        if Tracking.objects.filter(
                day=self.get_previous_month_date(1),
                habit__in=user_habits).first():
            completed_months.append(previous_month)
        completed_months.append(self.months[int(self.get_month_number()) - 1])

        context['month_habits'] = Tracking.objects.filter(
            day__gte=f'{datetime.datetime.now().year}-{datetime.datetime.now().month}-01',
            habit__in=user_habits
        ).select_related('habit').order_by('day')
        context['habits_list'] = user_habits
        context['days'] = list(range(1, _get_days_in_month() + 1))
        context['title'] = 'Статистика привычек за месяц'
        context['months'] = completed_months
        return context


class StatisticPrevious(Statistic):
    """Страница со статистикой привычек за предыдущие месяца"""
    model = Tracking
    template_name = 'habits/statistic_previous.html'
    login_url = '/login/'

    def get_statistic(self, days: int, habits):
        statistic = {}
        for tracking in habits:
            if tracking.is_completed:
                if statistic.get(tracking.habit.name) is None:
                    statistic[tracking.habit.name] = 1
                else:
                    statistic[tracking.habit.name] += 1
        for h in statistic:
            statistic[h] = int((statistic[h] / days) * 100)
        return statistic

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_habits = Habits.objects.filter(user=self.request.user.id)

        month_num = self.get_month_number(self.kwargs["month"])
        if month_num in [11, 12]:
            first_day = f'{datetime.datetime.now().year - 1}-{month_num}-01'
            last_day = f'{datetime.datetime.now().year - 1}-{month_num}-{_get_days_in_month(num=self.kwargs["month"], year=1)}'

        else:
            first_day = f'{datetime.datetime.now().year}-{month_num}-01'
            last_day = f'{datetime.datetime.now().year}-{month_num}-{_get_days_in_month(self.kwargs["month"])}'
        context['month_habits'] = Tracking.objects.filter(
            day__range=(first_day, last_day),
            habit__in=user_habits
        ).select_related('habit').order_by('day')
        context['days'] = list(range(1, _get_days_in_month(self.kwargs["month"]) + 1))
        context['title'] = f'Статистика привычек за {self.get_month_name(month_num)}'
        context['progress'] = self.get_statistic(_get_days_in_month(self.kwargs["month"]), context['month_habits'])
        return context


@login_required(login_url='/login/')
def show_qr(request, habit_id):
    """Страница с отображением QR-кода привычки"""
    context = {'url': f'/media/habits_tracker/qr_images/{habit_id}.jpg',
               'title': '| QR-код привычки'}
    return render(request, 'habits/qr.html', context=context)


@login_required(login_url='/login/')
@require_http_methods(['POST'])
@csrf_exempt
def add(request):
    """Добавление новой привычки в БД"""
    _get_today_habits(request.user.id)
    name = request.POST['name']
    if len(name) == 0:
        return redirect('habits_tracker_index')
    user_id = request.user.id
    habit = Habits(name=name, user_id=user_id)
    habit.save()

    objects_list = []
    for d in range(1, _get_days_in_month() + 1):
        objects_list.append(Tracking(
            habit=habit,
            day=f'{datetime.datetime.now().year}-{datetime.datetime.now().month}-{d}')
        )
    Tracking.objects.bulk_create(objects_list)
    qr = qrcode.make(f'http://{ALLOWED_HOSTS}/update/{habit.id}/')
    qr.save(f'media/habits_tracker/qr_images/{habit.id}.jpg', 'JPEG')
    habit.qr = f'qr_images/{habit.id}.jpg'
    habit.save()
    return redirect('habits_tracker_index')


@login_required(login_url='/login/')
def update(request, habit_id):
    """Выполнение или отмена привычки"""
    habit = Tracking.objects.get(habit_id=habit_id, day=datetime.date.today())
    if request.user.id == habit.habit.user_id:
        habit.is_completed = not habit.is_completed
        habit.save()
    return HttpResponse(str(habit.is_completed), content_type="text/html")


@login_required(login_url='/login/')
def statistic_update(request, habit_id, day):
    """Выполнение или отмена привычки из страницы статистики"""
    habit = Tracking.objects.get(
        habit_id=habit_id,
        day=f'{datetime.datetime.now().year}-{datetime.datetime.now().month}-{day}')
    habit.is_completed = not habit.is_completed
    habit.save()
    return redirect('statistic')


@login_required(login_url='/login/')
def delete(request, habit_id):
    """Удаление привычки и соотвествующего QR-кода из БД"""
    habit = Habits.objects.get(id=habit_id)
    root_path = str(Path(__file__).resolve().parent.parent)
    os.remove(root_path + f'/media/habits_tracker/qr_images/{habit_id}.jpg')
    habit.delete()
    return redirect('habits_tracker_index')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена<h1>')

