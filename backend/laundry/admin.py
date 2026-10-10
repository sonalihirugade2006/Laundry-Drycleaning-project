
from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError

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


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        total = cleaned_data.get('total_amount')
        discount = cleaned_data.get('discount') or 0
        advance = cleaned_data.get('advance_amount') or 0

        if total is not None:
            if discount < 0 or advance < 0:
                raise ValidationError(
                    'Discount and advance amount cannot be negative.'
                )

            if discount + advance > total:
                raise ValidationError(
                    'Discount and advance cannot exceed the total amount.'
                )

            pending = total - discount - advance
            cleaned_data['pending_amount'] = pending

            if pending == 0:
                cleaned_data['payment_status'] = 'Paid'
            elif advance > 0 or discount > 0:
                cleaned_data['payment_status'] = 'Partial'
            else:
                cleaned_data['payment_status'] = 'Pending'

        return cleaned_data



class PaymentAdmin(admin.ModelAdmin):
    form = PaymentForm

    def save_model(self, request, obj, form, change):
        from django.utils import timezone

        if obj.payment_status == 'Paid':
            if not obj.payment_date:
                obj.payment_date = timezone.now()
        else:
            obj.payment_date = None

        super().save_model(request, obj, form, change)

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        order = cleaned_data.get('order')
        delivery_status = cleaned_data.get('delivery_status')

        if (
            order
            and delivery_status
            and delivery_status.strip().lower() == 'delivered'
            and order.status.strip().lower() not in ['ready', 'delivered']
        ):
            raise ValidationError(
                'The order must be Ready before delivery can be completed.'
            )

        return cleaned_data



class DeliveryAdmin(admin.ModelAdmin):
    form = DeliveryForm

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if obj.delivery_status.strip().lower() == 'delivered':
            order = obj.order

            if order.status != 'Delivered':
                order.status = 'Delivered'
                order.save(update_fields=['status'])

                Notification.objects.create(
                    user=order.customer.user,
                    order=order,
                    message=f"Your Order #{order.id} has been delivered successfully.",
                    notification_type='Delivery Update'
                )

admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Delivery, DeliveryAdmin)

@admin.register(ProcessingStage)
class ProcessingStageAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        from django.utils import timezone

        if obj.status == 'In Progress' and not obj.started_at:
            obj.started_at = timezone.now()

        if obj.status == 'Completed':
            if not obj.started_at:
                obj.started_at = timezone.now()

            if not obj.completed_at:
                obj.completed_at = timezone.now()

        super().save_model(request, obj, form, change)

        if obj.status == 'Completed':
            order = obj.order

            if obj.stage_name == 'Ready' and order.status != 'Ready':
                order.status = 'Ready'
                order.save(update_fields=['status'])

            elif obj.stage_name == 'Delivered' and order.status != 'Delivered':
                order.status = 'Delivered'
                order.save(update_fields=['status'])

admin.site.register(Payment, PaymentAdmin)
admin.site.register(Notification)