from django.shortcuts import render,redirect
# omkar changes 
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate , login , logout
from django.http import HttpResponse
from django.contrib import messages
from .models import Room,Topic,Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm  
#OMkar changes 
"""
rooms = [

{'id' :1 ,'name' : 'Room number 1 !!'},
{'id' :2 ,'name' : 'Room number 2 !!'},
{'id' :3 ,'name' : 'Room number 3 !!'}
]
"""


def loginpage(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try :
            user = User.objects.get(username=username) # check if user already exists in database in table User
        except:
            messages.error(request,'User does not exist')


        user = authenticate(request,username=username , password=password)  # check if username and password is correct

        if user is not None :
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,"Username or password is incorrect")

    context = {'page' : page}
    return render(request,'base/login_register.html',context)

def logoutpage(request):
    logout(request)
    return render(request,'base/home.html') 

def registerpage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # not commiting the user cedential changes becuase we want to do some validations on it before saving
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect ('home')
        else:
            messages.error(request,"Error occured during registration")


    context = {'form' : form}
    return render(request,'base/login_register.html',context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''   # We get this q parameter from URL link. Search functioanlity
    rooms = Room.objects.filter(Q(topic__name__icontains = q)   | 
                                  Q(name__icontains = q) | 
                                  Q(description__icontains = q)  
                                ) 
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q))
    context = {'rooms' : rooms , 'topics' : topics , 'room_count' : room_count,'room_messages':room_messages}
    return render(request, 'base/home.html',context)

def room(request,pk):
    # Omkar_1_start we are checking what id is passedi in url and displaying information specific for that id only 
    room = Room.objects.get(id=pk)  # Room.objects.get is used to retrieve specific row 
    room_messages = room.message_set.all() # _set is used to access child models. message is child of room
    participants = room.participants.all()
    if request.method == 'POST':
        # below code creates Message object using passed 3 parameters
        message = Message.objects.create(   
                user = request.user,
                room = room,
                body = request.POST.get('body')

        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)

    context = {'room' : room , 'room_messages':room_messages , 'participants':participants}
    return render(request, 'base/room.html',context)
    # Omkar_2_start


def profile(request,pk):
    user = User.objects.get(id=pk)
    topics = Topic.objects.all()
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    context = {'user' : user , 'topics' : topics , 'rooms' : rooms , 'room_messages' : room_messages}
    return render (request,'base/profile.html',context)
@login_required(login_url='login') # If user is not authenticated then it redirects to login page
def CreateRoom(request): # create operation out of CRUD
    form = RoomForm() # This RoomForm is defined in forms.py which is imported in this views.py
    if request.method  == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid() :
            form.save()
            return redirect('home')
    context = {'form' : form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def UpdateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance = room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here !!')

    if request.method == 'POST':
        form = RoomForm(request.POST,instance = room)
        if form.is_valid() :
            form.save()
            return redirect('home')
    context = {'form' : form}
    return render (request,'base/room_form.html',context)

@login_required(login_url='login')
def DeleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse('You are not allowed here !!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj' : room}
    return render (request,'base/delete.html',context)

@login_required(login_url='login')
def DeleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse('You are not allowed to dlete this !!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    context = {'obj' : message}
    return render (request,'base/delete.html',context)