from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.urls import reverse

User = get_user_model()

class Chat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats_as_user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats_as_user2")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {self.user1.nickname or self.user1.username} and {self.user2.nickname or self.user2.username}"

class Message(models.Model):
    context = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    reply_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name="replies")
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Message by {self.author.nickname or self.author.username} at {self.sent_at}"