
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from laundry.api_views import services_api
from laundry.views import (
    home,
    csrf_token_view,
    customer_addresses_api,
    register,
    login_view,
    dashboard,
    logout_view,
    profile,
    delete_address,
    services,
    place_order,
    create_order_api,
    my_orders,
    order_tracking,
    my_deliveries,
    my_payments,
    my_notifications,
    mark_notification_read,
    daily_orders_report,
    revenue_report,
)


urlpatterns = [
    path('api/csrf/', csrf_token_view, name='csrf_token'),
    path('api/addresses/', customer_addresses_api, name='customer_addresses_api'),
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
    path(
        'order-tracking/<int:order_id>/',
        order_tracking,
        name='order_tracking',
    ),
    path('my-deliveries/', my_deliveries, name='my_deliveries'),
    path('my-payments/', my_payments, name='my_payments'),
    path('my-notifications/', my_notifications, name='my_notifications'),
    path(
        'mark-notification-read/<int:notification_id>/',
        mark_notification_read,
        name='mark_notification_read',
    ),
    path(
        'daily-orders-report/',
        daily_orders_report,
        name='daily_orders_report',
    ),
    path('revenue-report/', revenue_report, name='revenue_report'),
        path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='laundry/password_reset.html'
        ),
        name='password_reset',
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='laundry/password_reset_done.html'
        ),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='laundry/password_reset_confirm.html'
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='laundry/password_reset_complete.html'
        ),
        name='password_reset_complete',
    ),
    path('api/services/', services_api, name='services_api'),
    path(
    'api/orders/',
    create_order_api,
    name='create_order_api'
    ),
]
