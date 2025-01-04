from django.urls import path
from .views import UserRegisterView, UserLoginView, UserProfileView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='user_profile'),
]