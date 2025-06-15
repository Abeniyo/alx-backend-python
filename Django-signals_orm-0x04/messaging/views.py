from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.cache import cache_page
from .models import Message
from .forms import MessageForm  # you need to create this form


def get_thread(message):
    q = Message.objects.filter(parent_message=message).select_related('sender', 'receiver').prefetch_related('replies')
    return q

@login_required
@cache_page(60)
def conversation(request, message_id):
    root = get_object_or_404(
        Message.objects.select_related('sender', 'receiver').prefetch_related('replies'),
        pk=message_id
    )
    replies = get_thread(root)
    return render(request, 'conversation.html', {'root': root, 'replies': replies})


@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            receiver = form.cleaned_data['receiver']
            content = form.cleaned_data['content']
            parent = form.cleaned_data.get('parent_message')

            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                content=content,
                parent_message=parent
            )
            messages.success(request, "Message sent!")
            return redirect('inbox')  # Replace with your inbox URL
    else:
        form = MessageForm()
    return render(request, 'send_message.html', {'form': form})


@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('home')  # update with your homepage URL name
    return render(request, 'delete_account.html')


@login_required
def inbox(request):
    messages_list = Message.objects.filter(receiver=request.user).select_related('sender').only('content', 'timestamp')
    return render(request, 'inbox.html', {'messages': messages_list})
