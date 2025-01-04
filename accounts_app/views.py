from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.views import View
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import CustomUserCreationForm
from .models import CustomUser
from .mixins import LoginRequiredPermissionMixin, RedirectAuthenticatedUserMixin


class UserRegisterView(RedirectAuthenticatedUserMixin, View):
    
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'accounts_app/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
        return render(request, 'accounts_app/register.html', {'form': form})

class UserLoginView(RedirectAuthenticatedUserMixin, LoginView):
    template_name = 'accounts_app/login.html'
    redirect_authenticated_user = True


class UserProfileView(View):
    def get(self, request, username=None):
        if username:
            user = get_object_or_404(CustomUser, username=username)
            if user.is_private and user != request.user:  # Перевірка приватності
                return HttpResponseForbidden("Цей профіль приватний.")
            return render(request, 'accounts_app/profile.html', {'user': user})
        return render(request, 'accounts_app/profile.html', {'user': request.user})

    def post(self, request, username=None):
        user = request.user
        if username and user.username != username:
            return HttpResponseForbidden("Ви не можете змінювати цей профіль.")

        # Оновлення статусу приватності
        is_private = request.POST.get('is_private') == 'on'
        user.is_private = is_private
        user.save()

        # Повідомлення про успіх
        messages.success(request, "Налаштування профілю оновлено.")
        return redirect('user_profile', username=user.username)