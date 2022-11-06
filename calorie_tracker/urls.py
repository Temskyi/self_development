from django.urls import path

from .views import *

urlpatterns = [
    path('', DishList.as_view(), name='calorie_counter_index'),
    path('dish-list/', DishList.as_view(), name='dish_list'),
    path('dish-add/', dish_add_view, name='dish_add'),
    path('dish-details/<int:dish_id>/', dish_details_view, name='dish_details')
]
