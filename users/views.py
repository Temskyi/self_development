from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from .forms import *
from .models import CustomUser
from django.db import IntegrityError


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'users/register.html', {
                'message': 'Passwords must match.',
            })

        # Attempt to create new user
        try:
            user = CustomUser.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'users/register.html', {
                'message': 'Username already taken.',
            })
        login(request, user)
        return HttpResponseRedirect(reverse('users_index'))
    else:
        return render(request, 'users/register.html')



# class RegisterUser(CreateView):
#     form_class = RegisterUserForm
#     template_name = 'users/register.html'
#     success_url = reverse_lazy('index')
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Регистрация'
#         return context
#
#     def form_invalid(self, form):
#         return self.render_to_response(self.get_context_data(
#             form=form,
#             message='Введены неверные данные.'))
#
#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('users_index')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(
            form=form,
            message='Неверное имя пользователя и / или пароль.'))

    def get_success_url(self):
        return reverse_lazy('users_index')


def logout_user(request):
    logout(request)
    return redirect('login')


def users_index(request):
    return render(request, 'users/users_index.html')

