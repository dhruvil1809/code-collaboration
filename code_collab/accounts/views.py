from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from projects.models import Project
from django.urls import reverse

def register(request):
    errors = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            errors['password_mismatch'] = "Passwords do not match"
        elif User.objects.filter(username=username).exists():
            errors['username_exists'] = "Username already exists"
        elif User.objects.filter(email=email).exists():
            errors['email_exists'] = "Email already in use"
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            login(request, user)
            return redirect('home')
        
    return render(request, 'accounts/register.html', {'errors': errors})

def user_login(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Invalid username or password" 

    return render(request, 'accounts/login.html', {'error_message': error_message})

def verify_email(request):
    error_message = None
    if request.method == 'POST':
        email = request.POST.get('email')

        if User.objects.filter(email=email).exists():
            reset_password_url = reverse('reset_password', kwargs={'email': email})
            return redirect(reset_password_url)
        else:
            error_message = "Email not found"

    return render(request, 'accounts/verify_email.html', {'error_message': error_message})

def reset_password(request, email):
    error_message = None
    user = User.objects.get(email=email)

    if request.method == 'POST':
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            error_message = "Passwords do not match"
        else:
            user.set_password(password)
            user.save()
            return redirect('login')
    
    return render(request, 'accounts/reset_password.html', {'email': email,'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):

    try:
        user = request.user
        
        # Filter projects where the user is either the owner or a collaborator
        owned_projects = Project.objects.filter(user=user)
        collaborated_projects = Project.objects.filter(collaborators=user)
        
        # Combine the two QuerySets and remove duplicates
        projects = owned_projects | collaborated_projects
        projects = projects.distinct()
    
    except Exception as e:
        projects = Project.objects.all()

        return render(request, 'accounts/home.html', {'projects': projects})
    
    return render(request, 'accounts/home.html', {'projects': projects})
