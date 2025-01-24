from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['context', 'reply_to']
        widgets = {
            'context': forms.Textarea(attrs={'placeholder': 'Enter your message here...', 'rows': 3}),
        }