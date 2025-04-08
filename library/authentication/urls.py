from django.urls import path
from authentication import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('users/', views.users_list, name='users_list'),
    path('users/<int:user_id>/', views.user_details, name='user_details'),
    # Api | Users
    path('api/v1/user/<int:id>/', views.UserDetailView.as_view(), name='user-detail'),
    path('api/v1/user/create/', views.UserCreateView.as_view(), name='create_user'),
    # Api | User's order
    path('api/v1/user/<int:id>/orders/', views.UserOrderListView.as_view(), name='user_orders'),
    path('api/v1/user/<int:id>/order/<int:order_id>/', views.UserOrderDetailView.as_view(), name='user_order_detail'),
    path('api/v1/user/<int:id>/order/', views.UserOrderCreateView.as_view(), name='user_order_create'),

]
