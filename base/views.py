from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q, Count
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from base import models, forms


def login_page(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = get_user_model().objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        messages.error(request, 'Email or password does not exist')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def register_user(request):
    page = 'register'
    form = forms.UserRegisterForm()
    if request.method == 'POST':
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        messages.error(request, 'Something went wrong!')
    context = {'page': page, 'form': form}
    return render(request, 'base/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = models.Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = models.Topic.objects.all() \
        .annotate(num_rooms=Count('room')) \
        .order_by('-num_rooms')[:3]
    room_count = rooms.count()
    room_messages = models.Message.objects.filter(
        Q(room__name__icontains=q) |
        Q(room__topic__name__icontains=q)
    )
    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = models.Room.objects.filter(pk=pk)
    room_obj = room[0] if room.exists() else None
    if room_obj:
        room_messages = room_obj.message_set.all()
        participants = room_obj.participants.all()

    if request.method == 'POST':
        message = models.Message.objects.create(
            user=request.user,
            room=room_obj,
            body=request.POST.get('body')
        )
        room_obj.participants.add(request.user)
        return redirect('room', pk=room_obj.id)
    context = {'room': room_obj, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)


@login_required(login_url='/login')
def user_profile(request, pk):
    user = get_user_model().objects.get(pk=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = models.Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='/login')
def create_room(request):
    form = forms.RoomForm()
    topics = models.Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = models.Topic.objects.get_or_create(name=topic_name)
        models.Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='/login')
def update_room(request, pk):
    room = models.Room.objects.get(id=pk)
    topics = models.Topic.objects.all()
    form = forms.RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = models.Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='/login')
def delete_room(request, pk):
    room = models.Room.objects.get(pk=pk)
    context = {'obj': room}

    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', context)


@login_required(login_url='/login')
def delete_message(request, pk):
    message = models.Message.objects.get(pk=pk)
    room_id = message.room.id
    context = {'obj': message}

    if request.user != message.user:
        return HttpResponse('You are not allowed to do it')

    if request.method == 'POST':
        message.delete()
        return redirect('room', pk=room_id)

    return render(request, 'base/delete.html', context)


@login_required(login_url='/login')
def edit_user(request):
    form = forms.UserForm(instance=request.user)
    context = {'form': form}
    if request.method == 'POST':
        form = forms.UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=request.user.pk)
    return render(request, 'base/edit-user.html', context)


def topics_page(request):
    topics = models.Topic.objects.filter(name__icontains=request.GET.get('q', ''))
    context = {'topics': topics}
    return render(request, 'base/topics.html', context)

def activity_page(request):
    room_messages = models.Message.objects.all()[:3]
    context = {'room_messages': room_messages}
    return render(request, 'base/activity.html', context)