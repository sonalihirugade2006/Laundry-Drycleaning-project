from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Customer, Address, Service, Order, OrderItem, ProcessingStage, Delivery, Payment, Notification

def home(request):
    return render(request, 'laundry/home.html')

def services(request):

    all_services = Service.objects.all()

    return render(
        request,
        'laundry/services.html',
        {
            'services': all_services
        }
    )

@login_required
def place_order(request):

    customer = Customer.objects.get(user=request.user)

    services = Service.objects.all()
    addresses = Address.objects.filter(customer=customer)

    if request.method == 'POST':

        service_id = request.POST.get('service')
        address_id = request.POST.get('address')
        garment_type = request.POST.get('garment_type')
        quantity = int(request.POST.get('quantity'))
        condition = request.POST.get('condition')
        expected_date = request.POST.get('expected_date')
        special_instructions = request.POST.get('special_instructions')

        service = Service.objects.get(id=service_id)
        address = Address.objects.get(
            id=address_id,
            customer=customer
        )

        total_amount = service.price_per_item * quantity

        order = Order.objects.create(
            customer=customer,
            address=address,
            expected_date=expected_date,
            special_instructions=special_instructions,
            total_amount=total_amount
        )
        
        stage_names = [
            'Received',
            'Sorting',
            'Washing',
            'Drying',
            'Ironing',
            'Quality Check',
            'Ready',
            'Delivered'
        ]

        for stage_name in stage_names:
            ProcessingStage.objects.create(
                order=order,
                stage_name=stage_name,
                status='Pending'
            )


        OrderItem.objects.create(
            order=order,
            service=service,
            garment_type=garment_type,
            quantity=quantity,
            condition=condition,
            price_at_order=service.price_per_item
        )

        Payment.objects.create(
            order=order,
            total_amount=total_amount,
            discount=0,
            advance_amount=0,
            pending_amount=total_amount,
            payment_status='Pending'
        )
        Notification.objects.create(
            user=request.user,
            order=order,
            message=f"Your Order #{order.id} has been received successfully.",
            notification_type='Order Received'
        )

        return redirect('/dashboard/')

    return render(
        request,
        'laundry/place_order.html',
        {
            'services': services,
            'addresses': addresses
        }
    )


def register(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(
                request,
                'laundry/register.html',
                {'error': 'Passwords do not match.'}
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                'laundry/register.html',
                {'error': 'Username already exists.'}
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Customer.objects.create(
            user=user,
            name=username,
            phone='Not provided'
        )

        return redirect('/login/')

    return render(request, 'laundry/register.html')


def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            auth_login(request, user)
            return redirect('/dashboard/')

        return render(
            request,
            'laundry/login.html',
            {'error': 'Invalid username or password.'}
        )
       
    return render(request, 'laundry/login.html')

@login_required
def dashboard(request):
    unread_count = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    return render(
        request,
        'laundry/dashboard.html',
        {
            'unread_count': unread_count
        }
    )


@login_required
def my_orders(request):

    customer = Customer.objects.get(user=request.user)

    orders = Order.objects.filter(
        customer=customer
    ).order_by('-order_date')

    return render(
        request,
        'laundry/my_orders.html',
        {
            'orders': orders
        }
    )
@login_required
def order_tracking(request, order_id):

    customer = Customer.objects.get(user=request.user)

    order = Order.objects.get(
        id=order_id,
        customer=customer
    )

    stages = ProcessingStage.objects.filter(
        order=order
    ).order_by('id')

    return render(
        request,
        'laundry/order_tracking.html',
        {
            'order': order,
            'stages': stages
        }
    )

@login_required
def profile(request):

    customer = Customer.objects.get(user=request.user)

    if request.method == 'POST':

        address_line = request.POST.get('address_line')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')

        Address.objects.create(
            customer=customer,
            address_line=address_line,
            city=city,
            pincode=pincode
        )

    addresses = Address.objects.filter(customer=customer)

    return render(
        request,
        'laundry/profile.html',
        {
            'customer': customer,
            'addresses': addresses
        }
    )

def logout_view(request):
    logout(request)
    return redirect('/login/')

@login_required
def my_deliveries(request):
    customer = Customer.objects.get(user=request.user)

    deliveries = Delivery.objects.filter(
        order__customer=customer
    ).select_related(
        'order',
        'address',
        'delivery_staff'
    ).order_by('-id')

    return render(
        request,
        'laundry/my_deliveries.html',
        {'deliveries': deliveries}
    )

@login_required
def my_payments(request):
    customer = Customer.objects.get(user=request.user)

    payments = Payment.objects.filter(
        order__customer=customer
    ).select_related(
        'order'
    ).order_by('-id')

    return render(
        request,
        'laundry/my_payments.html',
        {'payments': payments}
    )
@login_required
def my_notifications(request):
    notifications = Notification.objects.filter(
        user=request.user
    ).select_related('order').order_by('-created_at')

    return render(
        request,
        'laundry/my_notifications.html',
        {'notifications': notifications}
    )
    
@login_required
def mark_notification_read(request, notification_id):
    notification = Notification.objects.get(
        id=notification_id,
        user=request.user
    )
    notification.is_read = True
    notification.save(update_fields=['is_read'])

    return redirect('/my-notifications/')

