from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import MessageForm
from .models import Chat, Message
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def chat_list_view(request):
    user_chats = Chat.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    ).distinct()

    selected_chat_id = request.GET.get('chat_id')
    selected_chat = None
    messages_in_chat = []

    if selected_chat_id:
        selected_chat = get_object_or_404(Chat, id=selected_chat_id)
        if request.user not in [selected_chat.user1, selected_chat.user2]:
            messages.error(request, "Access denied.")
            return redirect('chat_view')

        messages_in_chat = selected_chat.messages.filter(is_deleted=False).order_by('sent_at')

    form = MessageForm()

    context = {
        'user_chats': user_chats,
        'selected_chat': selected_chat,
        'messages_in_chat': messages_in_chat,
        'form': form,
    }
    return render(request, 'chat_app/chat_list.html', context)

@login_required
def delete_message_view(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if message.author != request.user:
        messages.error(request, "Ти можеш видаляти тільки свої повідомлення.")
        return redirect('chat_view')

    message.is_deleted = True
    message.save()
    messages.success(request, "Повідомлення видалено.")
    return redirect(f'/chat?chat_id={message.chat.id}')


@login_required
def reply_to_message_view(request, message_id):
    replied_message = get_object_or_404(Message, id=message_id)

    if request.user not in [replied_message.chat.user1, replied_message.chat.user2]:
        messages.error(request, "Ви не маєте доступу до цього чату.")
        return redirect('chat_list')

    request.session['reply_to'] = replied_message.id
    return redirect(f'/chat/?chat_id={replied_message.chat.id}')


@login_required
def send_message_view(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    if request.user not in [chat.user1, chat.user2]:
        messages.error(request, "Ви не маєте доступу до цього чату.")
        return redirect('chat_list')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.chat = chat

            reply_to_id = request.session.pop('reply_to', None)
            if reply_to_id:
                reply_to_message = Message.objects.filter(id=reply_to_id).first()
                if reply_to_message and reply_to_message.chat == chat:
                    message.reply_to = reply_to_message

            message.save()
            return redirect(f'/chat/?chat_id={chat.id}')
        else:
            messages.error(request, "Помилка при надсиланні повідомлення. Перевірте форму.")
    else:
        form = MessageForm()

    context = {
        'form': form,
        'chat': chat,
    }
    return render(request, 'chat_app/send_message.html', context)