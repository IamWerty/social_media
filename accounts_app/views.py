from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views import View
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


class UserProfileView(LoginRequiredPermissionMixin, View):
    def get(self, request):
        return render(request, 'accounts_app/profile.html', {'user': request.user})