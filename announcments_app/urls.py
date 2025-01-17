from django.urls import path
from . import views

urlpatterns = [
    path('anns/', views.Announcment_list, name='Announcment_list'),
    path('anns/<int:pk>/', views.AnnouncmentDetailView.as_view(), name='Announcment_detail'),
    path('anns/create/', views.AnnouncmentCreateView.as_view(), name='Announcment_create'),
    path('anns/<int:pk>/update/', views.AnnouncmentUpdateView.as_view(), name='Announcment_update'),
    path('anns/<int:pk>/delete/', views.AnnouncmentDeleteView.as_view(), name='Announcment_delete'),
]
