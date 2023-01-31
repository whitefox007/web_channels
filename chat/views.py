from django.shortcuts import render
from .models import Chat

# Create your views here.

def lobby(request):
    chats = Chat.objects.all()
    return render(request, 'chat/lobby.html', {'chats': chats})
