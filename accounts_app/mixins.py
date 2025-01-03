from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect



class LoginRequiredPermissionMixin(LoginRequiredMixin):
    """Міксин для перевірки, що користувач залогінений."""
    login_url = '/login/'

class RedirectAuthenticatedUserMixin(AccessMixin):
    """Міксин для перенаправлення залогінених користувачів."""
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile', request.user.username)
        return super().dispatch(request, *args, **kwargs)