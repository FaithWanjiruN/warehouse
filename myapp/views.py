
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.db.models import Sum
from django.contrib.auth import update_session_auth_hash #new

# Create your views here.
#loginpage
def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username= username, password= password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.error(request,'Username/Password is incorrect')
            return redirect('login')
    else:
        return render(request,"login.html")
    
	#registerpage

def logout(request):
    auth.logout(request)
    return redirect('/')

#registers profile for user
def profile(request):
    u = request.user
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['fn']
        last_name = request.POST['ln']
        email = request.POST['email']
        old = request.POST['old']
        new = request.POST['new']
        user = User.objects.get(pk = u.pk)        
            
        if User.objects.filter(username=username).exclude(pk=u.pk).exists():
            messages.error(request,'Username already exists')
        
        elif User.objects.filter(email=email).exclude(pk=u.pk).exists():
                messages.error(request,'Email already exists')
        
        elif user.check_password(old):
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.set_password(new)
            user.save()
            
            #update session
            update_session_auth_hash(request, user)

            messages.success(request,'Profile updated')
        else:
            messages.error(request,'Wrong Old Password')
            
        return redirect('user')
    
    else:
        user = request.user
        return render(request,"user.html")
    
def bookings(request):
    user = request.user
    book = Bookings.objects.filter(user=user.pk)
    return render(request,"bookings.html", {'book':book} )

def dashboard(request):
    user = request.user
    m = Shows.objects.filter(cinema=user.cinema).values('movie','movie__movie_name','movie__movie_poster').distinct()
    print(m)
    return render(request,"dashboard.html", {'list':m})

def earnings(request):
    user = request.user
    d = Bookings.objects.filter(shows__cinema=user.cinema)
    total = Bookings.objects.filter(shows__cinema=user.cinema).aggregate(Sum('shows__price'))
    return render(request,"earnings.html", {'s':d, 'total':total})
