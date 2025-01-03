from django.urls import path
from .views import ProfileView, RegisterView, UserLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]