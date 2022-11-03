from django.contrib import admin
from .models import Habits, Tracking


class HabitsAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_display_links = ('name',)
    list_filter = ('name', 'user')


class TrackingAdmin(admin.ModelAdmin):
    list_display = ('habit', 'is_completed', 'day', 'habit_user')
    list_display_links = ('habit',)
    list_filter = ('habit', 'day')

    def habit_user(self, obj):
        return obj.habit.user


admin.site.register(Habits, HabitsAdmin)
admin.site.register(Tracking, TrackingAdmin)