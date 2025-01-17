from django.shortcuts import render
from .models import Announcment
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

def Announcment_list(request):
    anns = Announcment.objects.all().order_by('-created_at')
    latest_anns = anns.first() if anns.exists() else None
    return render(request, 'Announcment_app/Announcment_list.html', {'anns': anns, 'latest_anns': latest_anns})

class AnnouncmentDetailView(DetailView):
    model = Announcment
    template_name = 'Announcment_app/Announcment_detail.html'
    context_object_name = 'ann'

class AnnouncmentCreateView(CreateView):
    model = Announcment
    template_name = 'Announcment_app/Announcment_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('Announcment_list')

class AnnouncmentUpdateView(UpdateView):
    model = Announcment
    template_name = 'Announcment_app/Announcment_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('Announcment_list')

class AnnouncmentDeleteView(DeleteView):
    model = Announcment
    template_name = 'Announcment_app/Announcment_confirm_delete.html'
    success_url = reverse_lazy('Announcment_list')