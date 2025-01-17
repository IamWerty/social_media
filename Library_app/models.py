from django.db import models
from django.urls import reverse
from accounts_app.models import CustomUser
from ckeditor.fields import RichTextField

class Book(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='books')
    date_upload = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=255, blank=True, help_text="Enter tags separated by commas")
    rates = models.FloatField(default=0.0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': self.pk})

class BookVote(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    value = models.IntegerField()  # 1 for upvote, -1 for downvote

    class Meta:
        unique_together = ('book', 'user')

class BookComment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='book_comments')
    content = models.TextField()
    rates = models.FloatField(default=0)
    date_upload = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"Comment by {self.author} on {self.book}"
    
    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': self.book.pk})

class BookCommentVote(models.Model):
    comment = models.ForeignKey(BookComment, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    value = models.IntegerField()

    class Meta:
        unique_together = ('comment', 'user')

class Chapter(models.Model):
    title = models.CharField(max_length=200)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapters')
    content = RichTextField()
    note = models.TextField(blank=True, null=True)
    rates = models.IntegerField(default=0)

    def __str__(self):
        return f"Chapter of {self.book.title}"
    
    def get_absolute_url(self):
        return reverse('chapter_detail', kwargs={'book_id': self.book.id, 'pk': self.pk})
    
class ChapterVote(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    value = models.IntegerField()

    class Meta:
        unique_together = ('chapter', 'user')

class ChapterComment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='chapter_comments')
    content = models.TextField()
    rates = models.FloatField(default=0.0)
    date_upload = models.DateTimeField(auto_now_add=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"Comment by {self.author} on Chapter of {self.chapter.book.title}"

class Channel(models.Model):
    name = models.CharField(max_length=255)
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='owned_channel')
    admins = models.ManyToManyField(CustomUser, related_name='admin_channels', blank=True)
    members = models.ManyToManyField(CustomUser, related_name='member_channels', blank=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="posts")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    reposted_book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True, related_name="repost_posts")
    reposted_chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True, blank=True, related_name="repost_posts")
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Post by {self.author} in {self.channel}"

class Repost(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='reposts')
    original_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reposts')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reposts')
    comment = models.TextField(blank=True, null=True)
    date_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Repost by {self.author} in {self.channel}"

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
