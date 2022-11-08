from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView
from django import forms

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
            print(dish_form.cleaned_data)
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
