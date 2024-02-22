# chat/views.py
from django.shortcuts import get_object_or_404, render, redirect
from .models import ChatRoom

def index(request):
    rooms = ChatRoom.objects.all()
    return render(request, 'chat/index.html', {'rooms': rooms})

def room(request, room_name):
    if not request.user.is_authenticated:
        return redirect('account:account_view')
    get_object_or_404(ChatRoom, name=room_name)
    return render(request, "chat/room.html", {"room_name": room_name})
