from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Library_app.models import Post, Book, Channel
from accounts_app import models
from announcments_app.models import Announcment 

@login_required
def writers_dashboard(request):
    user = request.user

    subscribed_channels = user.channels.all()
    latest_posts = Post.objects.filter(channel__in=subscribed_channels).order_by('-created_at')[:5]

    top_books = Book.objects.order_by('-rates')[:3]

    top_communities = Channel.objects.annotate(member_count=models.Count('members')).order_by('-member_count')[:3]

    last_announcement = Announcment.objects.order_by('-created_at').first()

    context = {
        'latest_posts': latest_posts,
        'top_books': top_books,
        'top_communities': top_communities,
        'last_announcement': last_announcement,
    }

    return render(request, 'index.html', context)
