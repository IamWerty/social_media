from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from django.contrib import messages
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse, reverse_lazy
from .models import Book, BookComment, Chapter, ChapterComment, Channel, Post, Repost, CustomUser, BookVote, ChapterVote, BookCommentVote

class BookListView(ListView):
    model = Book
    template_name = 'Library_app/book_list.html'
    context_object_name = 'books'

class BookCreateView(CreateView):
    model = Book
    fields = ['title', 'content', 'tags']
    template_name = 'Library_app/book_form.html'
    success_url = reverse_lazy('book_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BookDetailView(DetailView):
    model = Book
    template_name = 'Library_app/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context['owned_channel'] = getattr(user, 'owned_channel', None)
            context['admin_channels'] = user.admin_channels.all()
        else:
            context['owned_channel'] = None
            context['admin_channels'] = []
        return context

class BookCommentCreateView(CreateView):
    model = BookComment
    fields = ['content']
    template_name = 'Library_app/book_comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.book = get_object_or_404(Book, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.kwargs['pk']})

class ChapterCreateView(CreateView):
    model = Chapter
    fields = ['title','content', 'note']
    template_name = 'Library_app/chapter_form.html'

    def form_valid(self, form):
        book = get_object_or_404(Book, id=self.kwargs['book_id'])
        form.instance.book = book
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('book_detail', kwargs={'pk': self.kwargs['book_id']})
    
class ChapterDetailView(DetailView):
    model = Chapter
    template_name = 'Library_app/chapter_detail.html'
    context_object_name = 'chapter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = self.kwargs.get('book_id')
        context['book'] = get_object_or_404(Book, id=book_id)
        user = self.request.user
        if user.is_authenticated:
            context['owned_channel'] = getattr(user, 'owned_channel', None)
            context['admin_channels'] = user.admin_channels.all()
        else:
            context['owned_channel'] = None
            context['admin_channels'] = []
        return context

class ChapterCommentCreateView(CreateView):
    model = ChapterComment
    fields = ['content']
    template_name = 'Library_app/chapter_comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.chapter = get_object_or_404(Chapter, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('chapter_detail', kwargs={'book_id': self.object.chapter.book.id, 'pk': self.object.chapter.id})

class ChannelListView(ListView):
    model = Channel
    template_name = 'Library_app/channel_list.html'
    context_object_name = 'channels'

class ChannelCreateView(CreateView):
    model = Channel
    fields = ['name']
    template_name = 'Library_app/channel_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        channel = form.save()
        channel.admins.add(self.request.user)
        channel.members.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('channel_list')

class ChannelDetailView(DetailView):
    model = Channel
    template_name = 'Library_app/channel_detail.html'
    context_object_name = 'channel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_users'] = CustomUser.objects.all()
        context['posts'] = self.object.posts.all().order_by('-id')
        return context

class ManageAdminView(View):
    def post(self, request, pk):
        channel = get_object_or_404(Channel, pk=pk)
        username = request.POST.get('username')
        action = request.POST.get('action')

        if not request.user in channel.admins.all():
            messages.error(request, 'You do not have permission to manage admins.')
            return redirect('channel_detail', pk=pk)

        user = CustomUser.objects.filter(username=username).first()
        if not user:
            messages.error(request, 'User not found.')
            return redirect('channel_detail', pk=pk)

        if action == 'add':
            if user not in channel.admins.all():
                channel.admins.add(user)
                messages.success(request, f'User "{username}" added as admin.')
            else:
                messages.info(request, f'User "{username}" is already an admin.')
        elif action == 'remove':
            if user in channel.admins.all():
                channel.admins.remove(user)
                messages.success(request, f'User "{username}" removed from admins.')
            else:
                messages.info(request, f'User "{username}" is not an admin.')

        return redirect('channel_detail', pk=pk)

class RepostBookView(View):
    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        channel_id = request.POST.get("channel_id")
        comment = request.POST.get("comment", "").strip()
        channel = get_object_or_404(Channel, id=channel_id, owner=request.user)

        Post.objects.create(
            channel=channel,
            author=request.user,
            reposted_book=book,
            comment=comment,
            content=f"{request.user.username} Reposted {book.title}"
        )
        return redirect('channel_detail', pk=channel.id)

class RepostChapterView(View):
    def post(self, request, chapter_id):
        chapter = get_object_or_404(Chapter, id=chapter_id)
        channel_id = request.POST.get("channel_id")
        comment = request.POST.get("comment", "").strip()
        channel = get_object_or_404(Channel, id=channel_id, owner=request.user)

        Post.objects.create(
            channel=channel,
            author=request.user,
            reposted_chapter=chapter,
            comment=comment,
            content=f"{request.user.username} Reposted {chapter.title}"
        )
        return redirect('channel_detail', pk=channel.id)

class PostCreateView(CreateView):
    model = Post
    fields = ['content']
    template_name = 'Library_app/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.channel = get_object_or_404(Channel, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('channel_detail', kwargs={'pk': self.kwargs['pk']})

class RepostCreateView(View):
    def post(self, request, pk):
        channel = get_object_or_404(Channel, pk=pk)
        post_id = request.POST.get('post_id')
        original_post = get_object_or_404(Post, pk=post_id)

        if request.user in channel.members.all():
            Repost.objects.create(channel=channel, original_post=original_post, author=request.user)
            messages.success(request, 'Repost created successfully')
        else:
            messages.error(request, 'You do not have permission to repost in this channel')
        return redirect('channel_detail', pk=pk)
    
class VoteView(View):
    def post(self, request, obj_type, obj_id):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to vote.")
            return redirect('login')

        value = int(request.POST.get('value'))
        if value not in [-1, 1]:
            messages.error(request, "Invalid vote value.")
            return redirect('book_list')

        if obj_type == 'book':
            return self.handle_book_vote(request, obj_id, value)
        elif obj_type == 'chapter':
            return self.handle_chapter_vote(request, obj_id, value)
        elif obj_type == 'comment':
            return self.handle_comment_vote(request, obj_id, value)
        else:
            messages.error(request, "Invalid object type.")
            return redirect('book_list')

    def handle_book_vote(self, request, book_id, value):
        book = get_object_or_404(Book, pk=book_id)

        if request.user == book.author:
            messages.error(request, "You cannot vote on your own book.")
            return redirect(book.get_absolute_url())

        vote, created = BookVote.objects.get_or_create(
            user=request.user,
            book=book,
            defaults={'value': value}
        )

        if created:
            book.rates += value
        else:
            if vote.value == value:
                messages.error(request, "You have already voted this way.")
                return redirect(book.get_absolute_url())
            else:
                book.rates += (value - vote.value)
                vote.value = value
                vote.save()

        book.save()
        messages.success(request, "Your vote was successfully recorded.")
        return redirect(book.get_absolute_url())

    def handle_chapter_vote(self, request, chapter_id, value):
        chapter = get_object_or_404(Chapter, pk=chapter_id)

        if request.user == chapter.book.author:
            messages.error(request, "You cannot vote on your own chapter.")
            return redirect(chapter.get_absolute_url())

        vote, created = ChapterVote.objects.get_or_create(
            user=request.user,
            chapter=chapter,
            defaults={'value': value}
        )

        if created:
            chapter.rates += value
        else:
            if vote.value == value:
                messages.error(request, "You have already voted this way.")
                return redirect(chapter.get_absolute_url())
            else:
                chapter.rates += (value - vote.value)
                vote.value = value
                vote.save()

        chapter.save()
        messages.success(request, "Your vote was successfully recorded.")
        return redirect(chapter.get_absolute_url())

    def handle_comment_vote(self, request, comment_id, value):
        comment = get_object_or_404(BookComment, pk=comment_id)

        if request.user == comment.author:
            messages.error(request, "You cannot vote on your own comment.")
            return redirect(comment.get_absolute_url())

        vote, created = BookCommentVote.objects.get_or_create(
            user=request.user,
            comment=comment,
            defaults={'value': value}
        )

        if created:
            comment.rates += value
        else:
            if vote.value == value:
                messages.error(request, "You have already voted this way.")
                return redirect(comment.get_absolute_url())
            else:
                comment.rates += (value - vote.value)
                vote.value = value
                vote.save()

        comment.save()
        messages.success(request, "Your vote was successfully recorded.")
        return redirect(comment.get_absolute_url())