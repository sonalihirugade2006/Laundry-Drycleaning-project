from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Customer,Address


def home(request):
    return render(request, 'laundry/home.html')


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
    return render(request, 'laundry/dashboard.html')

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
