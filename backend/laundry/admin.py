from django.contrib import admin

from .models import (
    Customer,
    Address,
    Service,
    Order,
    OrderItem,
    ProcessingStage,
    Delivery,
    Payment,
    Notification,
)

admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ProcessingStage)
admin.site.register(Delivery)
admin.site.register(Payment)
admin.site.register(Notification)