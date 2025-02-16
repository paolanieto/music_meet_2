from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Event, Topic, Message, Musician
from .forms import EventForm
# Create your views here.

#events = [
#   {'id':1, 'name':'Banda Fest'},
#   {'id':2, 'name':'Quincenera en Los Angeles'},
#   {'id':3, 'name':'Punk Rock Night, Calabasus: The Daffys'},
#]

def musician(request):
    musician = Musician.objects.get(id=pk)
    musician_messages = Musician.message_set.all()

# do not call this login() because there is a default function called login that we need
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # creates a session in the browser
            login(request, user)
            return redirect('home')
        else: 
            messages.error(request, 'Username or password does not exist')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    #page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # commit is false because we need to access the user right away
            # if for some reason the user added and uppercase in their name or email
            # we want to make sure that that's lowercase automatically
            # we need to have access to be able to clean this data
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    # this is how our search is extracted from what is passed to url
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # What this is is a query for our events
    events = Event.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    
    topics = Topic.objects.all()
    event_count = events.count()
    # Filtering down by the event topic name
    event_messages = Message.objects.filter(Q(event__topic__name__icontains=q))

    context = {'events': events, 'topics': topics,
     'event_count': event_count, 'event_messages': event_messages}
    return render(request, 'base/home.html', context)
# later on pk will be used as the primary key to query the
# database
def event(request, pk):
    #event = None
    #for i in events:
        #if i['id'] == int(pk):
            #event = i 
    event = Event.objects.get(id=pk)
    # We can query child objects of a specific event here
    # if we take the parent model (Event) to get all the children
    # all we have to get is the model name and put it in lowercase
    # says give us the entire set of messages related to this specific event
    event_messages = event.message_set.all().order_by('-created')
    participants = event.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user, 
            event = event,
            body = request.POST.get('body')
        )
        event.participants.add(request.user)
        return redirect('event', pk=event.id)

    context = {'event': event, 'event_messages': event_messages, 
    'participants': participants}
    return render(request, 'base/event.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    events = user.event_set.all()
    event_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'events': events, 'event_messages': event_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createEvent(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            # Step 2 in FixingEventForm 10_22_22
            event = form.save(commit=False)
            event.host = request.user
            event.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/event_form.html', context)

@login_required(login_url='login')
def updateEvent(request, pk):
    event = Event.objects.get(id=pk)
    form = EventForm(instance=event)

    if request.user != event.host:
        return HttpResponse('You are not authorized here!!')

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/event_form.html', context)

@login_required(login_url='login')
def deleteEvent(request, pk):
    event = Event.objects.get(id=pk)

    if request.user != event.host:
        return HttpResponse('You are not authorized here!!')
    
    if request.method == 'POST':
        event.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':event})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not authorized here!!')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})

