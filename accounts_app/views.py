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
        user = get_object_or_404(CustomUser, username=username) if username else request.user
        is_following = user.followers.filter(id=request.user.id).exists() if request.user.is_authenticated else False
        return render(request, 'accounts_app/profile.html', {'user': user, 'is_following': is_following})

    def post(self, request, username=None):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Тільки авторизовані користувачі можуть підписуватися.")

        target_user = get_object_or_404(CustomUser, username=username)

        if target_user == request.user:
            messages.error(request, "Ви не можете підписатися на себе.")
            return redirect('user_profile', username=username)

        if target_user.followers.filter(id=request.user.id).exists():
            target_user.followers.remove(request.user)
            request.user.follows.remove(target_user)
            messages.info(request, f"Ви більше не підписані на {target_user.username}.")

            if target_user in request.user.friends.all():
                request.user.friends.remove(target_user)
                target_user.friends.remove(request.user)
                messages.info(request, f"Ви більше не друзі з {target_user.username}.")
        else:
            target_user.followers.add(request.user)
            request.user.follows.add(target_user)
            messages.success(request, f"Ви підписалися на {target_user.username}.")

            if request.user in target_user.followers.all():
                request.user.friends.add(target_user)
                target_user.friends.add(request.user)
                messages.success(request, f"Ви стали друзями з {target_user.username}.")

        return redirect('user_profile', username=username)

class UserProfileSettingsView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'accounts_app/settings.html', {'user': request.user})

    def post(self, request):
        user = request.user
        is_private = request.POST.get('is_private') == 'on'
        user.is_private = is_private
        user.save()

        messages.success(request, "Налаштування профілю оновлено.")
        return redirect('user_settings')

# Приклад використання різних тегів
# def my_view(request):
#     messages.success(request, 'Операція успішно виконана!')
#     messages.error(request, 'Сталася помилка.')
#     messages.info(request, 'Це інформаційне повідомлення.')
#     return render(request, 'your_template.html')