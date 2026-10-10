from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    preferences = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Address(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='addresses'
    )
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.customer.name} - {self.city}"

class Service(models.Model):
    service_name = models.CharField(max_length=100)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.service_name

class Order(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name='orders'
    )
    order_date = models.DateTimeField(auto_now_add=True)
    expected_date = models.DateField()
    special_instructions = models.TextField(blank=True)
    status = models.CharField(max_length=50, default='Received')
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"Order #{self.id}"    


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name='order_items'
    )
    garment_type = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    condition = models.CharField(max_length=255, blank=True)
    price_at_order = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.garment_type} - {self.quantity}"


class ProcessingStage(models.Model):
    STAGE_CHOICES = [
        ('Received', 'Received'),
        ('Sorting', 'Sorting'),
        ('Washing', 'Washing'),
        ('Drying', 'Drying'),
        ('Ironing', 'Ironing'),
        ('Quality Check', 'Quality Check'),
        ('Ready', 'Ready'),
        ('Delivered', 'Delivered'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='processing_stages'
    )
    stage_name = models.CharField(
        max_length=100,
        choices=STAGE_CHOICES
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.order} - {self.stage_name}"


class Delivery(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='deliveries'
    )
    delivery_staff = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deliveries'
    )
    pickup_date = models.DateTimeField(null=True, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)

    delivery_status = models.CharField(
        max_length=50,
        choices=[
            ('Scheduled', 'Scheduled'),
            ('Picked Up', 'Picked Up'),
            ('In Transit', 'In Transit'),
            ('Delivered', 'Delivered'),
            ('Cancelled', 'Cancelled'),
        ],
        default='Scheduled'
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name='deliveries'
    )

    def __str__(self):
        return f"Delivery for Order #{self.order.id}"


class Payment(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    advance_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    pending_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    payment_status = models.CharField(
        max_length=50,
        choices=[
            ('Pending', 'Pending'),
            ('Partial', 'Partial Payment'),
            ('Paid', 'Paid'),
        ],
        default='Pending'
    )
    payment_date = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Payment for Order #{self.order.id}"


class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.TextField()
    notification_type = models.CharField(max_length=50)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}" 