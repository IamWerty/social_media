from django.db import models
from django.urls import reverse
from accounts_app.models import CustomUser

class Book(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='books')
    date_upload = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=255, blank=True, help_text="Enter tags separated by commas")
    rates = models.FloatField(default=0.0)

    def __str__(self):
        return self.title

class BookComment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='book_comments')
    content = models.TextField()
    rates = models.FloatField(default=0.0)
    date_upload = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"Comment by {self.author} on {self.book}"

class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapters')
    content = models.TextField()
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Chapter of {self.book.title}"

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
    admins = models.ManyToManyField(CustomUser, related_name='admin_channels')
    members = models.ManyToManyField(CustomUser, related_name='member_channels')

    def __str__(self):
        return self.name

class Post(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    date_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.author} in {self.channel}"

class Repost(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='reposts')
    original_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reposts')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reposts')
    date_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Repost by {self.author} in {self.channel}"

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
