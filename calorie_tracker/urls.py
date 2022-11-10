from django.urls import path

from .views import *

urlpatterns = [
    path('', DishList.as_view(), name='calorie_counter_index'),
    path('dish-list/', DishList.as_view(), name='dish_list'),
    path('dish-add/', dish_add_view, name='dish_add'),
    path('dish-details/<int:dish_id>/', dish_details_view, name='dish_details'),

    path('today_meals/', TodayMeals.as_view(), name='today_meals'),
    path('today_meals/<int:meal_id>/', MealDetails.as_view(), name='meal_details'),
    path('today_meals/add_meal/', add_meal, name='add_meal'),
    path('today_meals/delete/<int:meal_id>/', delete_meal, name='delete_meal'),
    path('today_meals/add_product/<int:meal_id>/', add_product, name='add_product'),
    path('today_meals/<int:meal_id>/delete_product/<int:product_id>/', delete_product, name='delete_product'),

    path('history/', DaysHistory.as_view(), name='days_history'),
    path('history/<int:day_id>/', DayHistoryMeals.as_view(), name='day_history_meals'),
    path('history/<int:day_id>/<int:meal_id>/', DayHistoryMealProducts.as_view(), name='day_history_meal_products'),

    path('profile/weight/', weight_log_view, name='weight_log'),
    path('profile/weight/delete/<int:weight_id>/', weight_log_delete,
         name='weight_log_delete'),
]
