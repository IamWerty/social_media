from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views import View
from .models import CustomUser
from .form import CustomUserCreationForm
from .mixins import LoginRequiredPermissionMixin, RedirectAuthenticatedUserMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'accounts_app/profile.html', {'user': request.user})

class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'accounts_app/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile', username=user.username)
        return render(request, 'accounts_app/register.html', {'form': form})

class UserLoginView(RedirectAuthenticatedUserMixin, LoginView):
    template_name = "account_app/login.html"
    redirect_authenticated_user = True
