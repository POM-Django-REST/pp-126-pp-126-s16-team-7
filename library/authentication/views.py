from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseForbidden
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserSerializer, OrderSerializer
from rest_framework.exceptions import NotFound
from order.models import Order
from django.urls import reverse
from rest_framework import generics
from authentication.models import CustomUser
from authentication.forms import UserRegistrationForm, UserLoginForm, UserUpdateForm

def is_librarian(user):
    if user.role == 1:
        return True
    raise PermissionDenied("Доступ заборонено")

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
            role = int(form.cleaned_data["role"])

            if CustomUser.get_by_email(email):
                return render(request, "authentication/register.html", {"form": form, "error": "Email вже використовується"})
            user = CustomUser(
                email=email, 
                first_name=first_name, 
                middle_name=middle_name, 
                last_name=last_name,
                role = int(role))

            user.set_password(password) 
            user.is_active = True
            token = Token.objects.create(user=user)
            user.token = token
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
    if request.user.role == 0:
        return HttpResponseForbidden("🚫 You are not a librarian.")
    current_user = get_current_user(request)

    users = CustomUser.objects.all()
    return render(request, 'authentication/users_list.html', {'users': users})

@user_passes_test(is_librarian)
def user_details(request, user_id):
    current_user = get_current_user(request)

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


class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_object(self):
        try:
            return CustomUser.objects.get(id=self.kwargs['id'])
        except CustomUser.DoesNotExist:
            raise NotFound(detail="User not found.")

class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['id']
        return Order.objects.filter(user_id=user_id)
        
class UserOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Order.objects.get(user_id=self.kwargs['id'], id=self.kwargs['order_id'])
        except Order.DoesNotExist:
            raise NotFound(detail="Order not found.")

    def update(self, request, *args, **kwargs):
        # custom logic for updating order, if needed
        return super().update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        # custom logic for deleting order, if needed
        instance.delete()

class UserOrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = get_object_or_404(CustomUser, id=self.kwargs['id'])
        serializer.save(user=user)