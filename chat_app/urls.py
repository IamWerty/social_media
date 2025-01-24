from django.urls import path
from .views import chat_list_view, delete_message_view, send_message_view, reply_to_message_view

urlpatterns = [
    path('chat/', chat_list_view, name='chat_view'),
    path('send_message/<int:chat_id>/', send_message_view, name='send_message'),
    path('message/delete/<int:message_id>/', delete_message_view, name='delete_message'),
    path('reply/<int:message_id>/', reply_to_message_view, name='reply_to_message'),

]
