from django.shortcuts import render, redirect
from .forms import Carform
from .models import Car, Services, Auto_parts
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

def loginPage(request):
    page = 'login'     
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

       # try:
       #     user = User.objects.get(username=username)
       # except:
       #     messages.error(request, "User doesn't exist")
     
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "User or password isn't correct")

    context={'page': page}
    return render(request, 'Main/login_register.html', context)

def registerPage(request):
    form = UserCreationForm()
    page = 'register'
    if request.method =="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)   
            user.username = user.username
            user.save()
            login(request, user)   
            return redirect('home') 
    else:
        messages.error(request, 'An error occured during registration') 
 
    return render(request, 'Main/home.html' , {'form':form, 'page': page})


def logoutUser(request):
    logout(request)
    return redirect('home')

    

def search(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    cars = Car.objects.filter(Brand = q)
    car_count = cars.count()

    context = {'cars': cars, 'car_count': car_count}
    return render(request, 'Main/search.html', context)
    

def home(request):
    all_cars = Car.objects.all()

    # cars = Car.objects.filter(
    #     Q(Brand = q) |
    #     Q(user__User__icontains=q)
    #     )
    context = {'all_cars': all_cars}
    
    return render(request, 'Main/home.html', context)
    



@login_required(login_url='login')
def add_newcar(request):
    form = Carform()
    if request.method == 'POST':
        form = Carform(request.POST)
        if form.is_valid():
            Form = form.save(commit=False)
            Form.user = request.user
            Form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'Main/car-form.html', context)

@login_required(login_url='login')
def  update_car(request, pk):
    car = Car.objects.get(id = pk)
    form = Carform(instance=car)

    if request.user != car.user:
        return HttpResponse('You are not allowed to do this!') 
    
    if request.method == 'POST':
        form = Carform(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'Main/car-form.html', context)


@login_required(login_url='login')
def delete_car(request, pk):
    car = Car.objects.get(id=pk)


    if request.user != car.user: 
        return HttpResponse('You are not allowed to do this!')

    if request.method =='POST':
        car.delete()
        return redirect('home')

    return render(request, 'Main/delete.html', {'obj': car})