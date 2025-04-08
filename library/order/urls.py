from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_orders, name='all_orders'),              
    path('my/', views.my_orders, name='my_orders'),             
    path('create/', views.create_order, name='create_order'),
    path('update/<int:order_id>/', views.update_order, name='update_order'), 
    path('close/<int:order_id>/', views.close_order, name='close_order'),

    path('api/v1/orders/', views.OrderListView.as_view(), name='api_all_orders'),  
    path('api/v1/order/<int:id>/', views.OrderDetailView.as_view(), name='api_order_detail'),  
    path('api/v1/orders/my/', views.UserOrderListView.as_view(), name='api_my_orders'), 
]

