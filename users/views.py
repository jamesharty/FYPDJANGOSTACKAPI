from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages, auth
from django.contrib.auth.models import User
# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST['userName']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            return redirect('login')
    else:
        return render(request, 'login.html')

def register(request):
    if request.method =='POST':
        
        first_name = request.POST["first_name"]
        last_name = request.POST['last_name']
        username = request.POST['userName']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    return redirect('register')
                else:
                # Looks good
                    user = User.objects.create_user(username=username, password=password,email=email, first_name=first_name, last_name=last_name)
                    user.save()
                    return redirect('login')
        else:
            return redirect('register')
    else:
        return render(request, 'register.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('index')