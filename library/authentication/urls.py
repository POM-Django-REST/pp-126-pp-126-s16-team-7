from django.urls import path
from authentication import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('users/', views.users_list, name='users_list'),
    path('users/<int:user_id>/', views.user_details, name='user_details')
]
