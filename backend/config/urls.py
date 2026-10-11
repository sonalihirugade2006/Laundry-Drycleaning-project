
from django.contrib import admin
from django.urls import path
from laundry.views import (
    home,
    register,
    login_view,
    dashboard,
    logout_view,
    profile,
    delete_address,
    services,
    place_order,
    my_orders,
    order_tracking,
    my_deliveries,
    my_payments,
    my_notifications,
    mark_notification_read,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile, name='profile'),
    path(
    'delete-address/<int:address_id>/',
    delete_address,
    name='delete_address',
),
    path('logout/', logout_view, name='logout'),
    path('services/', services, name='services'),
    path('place-order/', place_order, name='place_order'),
    path('my-orders/', my_orders, name='my_orders'),
    path('order-tracking/<int:order_id>/', order_tracking, name='order_tracking'),
    path('my-deliveries/', my_deliveries, name='my_deliveries'),
    path('my-payments/', my_payments, name='my_payments'),
    path('my-notifications/', my_notifications, name='my_notifications'),
    path(
        'mark-notification-read/<int:notification_id>/',
        mark_notification_read,
        name='mark_notification_read',
    ),
]
