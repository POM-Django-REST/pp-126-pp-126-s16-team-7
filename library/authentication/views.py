from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

from django.http import HttpResponse
from django.urls import reverse
from authentication.models import CustomUser
from authentication.forms import UserRegistrationForm, UserLoginForm, UserUpdateForm

def get_current_user(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None
    return None

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            middle_name = form.cleaned_data["middle_name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            role = form.cleaned_data["role"]

            if CustomUser.get_by_email(email):
                return render(request, "authentication/register.html", {"form": form, "error": "Email вже використовується"})
            user = CustomUser.create(
                email=email, 
                password=password, 
                first_name=first_name, 
                middle_name=middle_name, 
                last_name=last_name)

            user.role = role
            user.is_active = True
            user.save()
            return redirect("login")

    else:
        form = UserRegistrationForm()

    return render(request, "authentication/register.html", {"form": form})

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                if user.role == 0 or user.role == 1:
                    auth_login(request, user)
                    return redirect('users_list')
                else:
                    form.add_error(None, "User role not allowed.")
                    return render(request, "authentication/login.html", {"form": form})
            else:
                form.add_error(None, "Invalid email or password.")
    else:
        form = UserLoginForm()
    
    return render(request, 'authentication/login.html', {'form': form})

def logout(request):
    request.session.flush()
    return redirect(reverse('login'))

def users_list(request):
    current_user = get_current_user(request)
    if not current_user or current_user.role != 1:
        return HttpResponse("Access denied. Librarians only.")
    users = CustomUser.objects.all()
    return render(request, 'authentication/users_list.html', {'users': users})

def user_details(request, user_id):
    current_user = get_current_user(request)
    if not current_user or current_user.role != 1:
        return HttpResponse("Access denied. Librarians only.")

    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        if "delete" in request.POST:
            user.delete()
            return redirect(reverse('users_list'))
        else:
            form = UserUpdateForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect(reverse('users_list'))
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'authentication/user_details.html', {'form': form, 'user': user})
