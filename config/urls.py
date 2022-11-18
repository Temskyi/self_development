"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import  static
from django.contrib import admin
from django.urls import path, include

from config import settings
from users.views import LoginUser, register, logout_user, users_index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', logout_user, name='logout'),
    path('login/', LoginUser.as_view(), name='login'),
    path('', users_index, name='users_index'),
    path('register/', register, name='register'),
    path('habits-tracker/', include('habits_tracker.urls')),
    path('calorie-tracker/', include('calorie_tracker.urls')),
    path('workout-tracker/', include('workout_tracker.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

