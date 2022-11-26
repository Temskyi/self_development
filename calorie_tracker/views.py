import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView
from django import forms
from users.models import CustomUser

from .models import *
from .forms import *


class DishList(LoginRequiredMixin, ListView):
    """Главная страница со списком доступных блюд"""
    model = Dish
    template_name = 'calorie_tracker/dish_list.html'
    login_url = '/login/'
    paginate_by = 4
    context_object_name = 'dishes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список блюд'
        return context

    def get_queryset(self):
        return Dish.objects.filter(Q(creator=self.request.user.id) | Q(creator=None))


def dish_details_view(request, dish_id):
    """Рендерит страницу, которая отображает детали выбранного блюда"""
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    dish = Dish.objects.get(id=dish_id)

    return render(request, 'calorie_tracker/dish_details.html', {'dish': dish})


@login_required
def dish_add_view(request):
    """Страница с добавлением нового блюда в БД"""

    if request.method == 'POST':
        dish_form = DishForm(request.POST, request.FILES)
        if dish_form.is_valid():
            new_dish = dish_form.save(commit=False)
            new_dish.creator = request.user
            new_dish.save()
            return render(request, 'calorie_tracker/dish_add.html', {
                'dish_form': DishForm(),
                'success': True
            })
        else:
            return render(request, 'calorie_tracker/dish_add.html',
                          {'dish_form': DishForm()})
    else:
        return render(request, 'calorie_tracker/dish_add.html',
                      {'dish_form': DishForm()})


class TodayMeals(LoginRequiredMixin, ListView):
    """Главная страница со списком доступных блюд"""
    model = Meal
    template_name = 'calorie_tracker/today_meals.html'
    login_url = '/login/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Сегодняшние приемы пищи'
        total_calories = 0
        total_protein = 0
        total_fat = 0
        total_carbohydrates = 0
        day = Day.objects.filter(day=datetime.date.today(),
                                 user=self.request.user.id).first()
        if not day:
            day = Day.objects.create(day=datetime.date.today(),
                                     user=self.request.user)
        meals = Meal.objects.filter(user=self.request.user.id, day=day)
        for meal in meals:
            total_calories += meal.total_calories
            total_protein = total_protein + float(meal.total_protein)
            total_fat = total_fat + float(meal.total_fat)
            total_carbohydrates = total_carbohydrates + float(meal.total_carbohydrates)
        context['meals'] = meals
        context['total_calories'] = total_calories
        context['total_protein'] = total_protein
        context['total_fat'] = total_fat
        context['total_carbohydrates'] = total_carbohydrates
        return context


class MealDetails(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'calorie_tracker/meal_details.html'
    login_url = '/login/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_form'] = ProductForm(user_id=self.request.user.id)
        context['title'] = 'Прием пищи'
        context['meal_id'] = self.kwargs['meal_id']
        meal = Meal.objects.get(id=self.kwargs['meal_id'])
        context['total_calories'] = meal.total_calories
        context['total_protein'] = meal.total_protein
        context['total_fat'] = meal.total_fat
        context['total_carbohydrates'] = meal.total_carbohydrates
        context['products'] = Product.objects.select_related('dish').filter(meal=meal)
        return context


@login_required
def add_meal(request):
    day = Day.objects.filter(day=datetime.date.today(),
                             user=request.user.id).first()
    new_meal = Meal.objects.create(user=request.user, day=day)
    return render(request, 'calorie_tracker/meal_details.html', {'meal_id': new_meal.id, 'product_form': ProductForm(user_id=request.user.id)})


@login_required
def delete_meal(request, meal_id):
    meal = Meal.objects.get(id=meal_id)
    day = meal.day
    day.total_calories -= meal.total_calories
    day.total_protein = float(day.total_protein) - float(meal.total_protein)
    day.total_fat = float(day.total_fat) - float(meal.total_fat)
    day.total_carbohydrates = float(day.total_carbohydrates) - float(meal.total_carbohydrates)
    meal.delete()
    return HttpResponseRedirect(reverse('today_meals'))


@login_required
def add_product(request, meal_id):
    """Страница с добавлением нового продукта в прием пищи"""

    if request.method == 'POST':
        product_form = ProductForm(request.user.id, request.POST)
        if product_form.is_valid():
            new_product = product_form.save(commit=False)
            new_product.meal = Meal.objects.get(id=meal_id)
            dish = new_product.dish
            new_product.calories = dish.calories * (new_product.weight / 100)
            new_product.protein = float(dish.protein) * (new_product.weight / 100)
            new_product.fat = float(dish.fat) * (new_product.weight / 100)
            new_product.carbohydrates = float(dish.carbohydrates) * (new_product.weight / 100)
            new_product.save()
            meal = Meal.objects.get(id=meal_id)
            meal.total_calories += new_product.calories
            meal.total_protein = float(meal.total_protein) + new_product.protein
            meal.total_fat = float(meal.total_fat) + new_product.fat
            meal.total_carbohydrates = float(meal.total_carbohydrates) + new_product.carbohydrates
            meal.save()
            day = meal.day
            day.total_calories = float(day.total_calories) + new_product.calories
            day.total_protein = float(day.total_protein) + new_product.protein
            day.total_fat = float(day.total_fat) + new_product.fat
            day.total_carbohydrates = float(day.total_carbohydrates) + new_product.carbohydrates
            day.save()
            return HttpResponseRedirect(f'/calorie-tracker/today_meals/{meal_id}/')
        else:
            return HttpResponseRedirect(f'/calorie-tracker/today_meals/{meal_id}/', {'fail': True})


@login_required
def delete_product(request, product_id, meal_id):
        product = Product.objects.get(id=product_id)
        meal = product.meal
        meal.total_calories -= product.calories
        meal.total_protein = float(meal.total_protein) - float(product.protein)
        meal.total_fat = float(meal.total_fat) - float(product.fat)
        meal.total_carbohydrates = float(meal.total_carbohydrates) - float(product.carbohydrates)
        meal.save()
        day = meal.day
        day.total_calories = float(day.total_calories) - float(product.calories)
        day.total_protein = float(day.total_protein) - float(product.protein)
        day.total_fat = float(day.total_fat) - float(product.fat)
        day.total_carbohydrates = float(day.total_carbohydrates) - float(product.carbohydrates)
        day.save()
        product.delete()
        return HttpResponseRedirect(f'/calorie-tracker/today_meals/{meal_id}/')


class DaysHistory(LoginRequiredMixin, ListView):
    model = Day
    template_name = 'calorie_tracker/day_history.html'
    login_url = '/login/'
    context_object_name = 'days'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'История'
        return context

    def get_queryset(self):
        days = Day.objects.filter(user=self.request.user.id).order_by('-day')
        return days


class DayHistoryMeals(LoginRequiredMixin, ListView):
    model = Meal
    template_name = 'calorie_tracker/day_history_meals.html'
    login_url = '/login/'
    context_object_name = 'meals'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        day = Day.objects.get(id=self.kwargs['day_id'])
        context['total_calories'] = day.total_calories
        context['total_protein'] = day.total_protein
        context['total_fat'] = day.total_fat
        context['total_carbohydrates'] = day.total_carbohydrates
        context['title'] = 'Приемы пищи за день'
        context['day_id'] = self.kwargs['day_id']
        return context

    def get_queryset(self):
        meals = Meal.objects.filter(day=self.kwargs['day_id'])
        return meals


class DayHistoryMealProducts(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'calorie_tracker/day_history_meal_products.html'
    login_url = '/login/'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        meal = Meal.objects.get(id=self.kwargs['meal_id'])
        context['total_calories'] = meal.total_calories
        context['total_protein'] = meal.total_protein
        context['total_fat'] = meal.total_fat
        context['total_carbohydrates'] = meal.total_carbohydrates
        context['title'] = 'Прием пищи'
        context['meal_id'] = self.kwargs['meal_id']
        context['day_id'] = self.kwargs['day_id']
        return context

    def get_queryset(self):
        products = Product.objects.filter(meal=self.kwargs['meal_id'])
        return products


@login_required
def weight_log_view(request):
    if request.method == 'POST':
        # get the values from the form
        try:
            weight = request.POST['weight']
            entry_date = request.POST['date']

            # get the currently logged in user
            user = request.user

            # add the data to the weight log
            weight_log = Weight(user=user, weight=weight, entry_date=entry_date)
            weight_log.save()
            custom_user = CustomUser.objects.get(id=request.user.id)
            custom_user.user_weight = weight
            custom_user.save()
        except:
            user_weight_log = Weight.objects.filter(user=request.user)
            custom_user = CustomUser.objects.get(id=request.user.id)
            user_weight = f'{int(custom_user.user_weight // 1)}.{int(str(custom_user.user_weight % 1)[2:4])}'
            return render(request, 'calorie_tracker/user_profile.html', {
                'user_weight_log': user_weight_log,
                'profile': True,
                'user_weight': user_weight,
                'form_error': True,
                'date': str(datetime.date.today())
            })


    # get the weight log of the logged in user
    user_weight_log = Weight.objects.filter(user=request.user)
    custom_user = CustomUser.objects.get(id=request.user.id)
    user_weight = f'{int(custom_user.user_weight // 1)}.{int(str(custom_user.user_weight % 1)[2:4])}'

    return render(request, 'calorie_tracker/user_profile.html', {
        'user_weight_log': user_weight_log,
        'profile': True,
        'user_weight': user_weight,
        'date': str(datetime.date.today())
    })


@login_required
def weight_log_delete(request, weight_id):
    # get the weight log of the logged in user
    weight_recorded = Weight.objects.filter(id=weight_id)

    if request.method == 'POST':
        weight_recorded.delete()
        return redirect('weight_log')

    return render(request, 'calorie_tracker/weight_log_delete.html', {'profile': True})

