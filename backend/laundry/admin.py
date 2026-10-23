
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

        total_amount = cleaned_data.get('total_amount')
        discount = cleaned_data.get('discount')
        advance_amount = cleaned_data.get('advance_amount')

        if (
            total_amount is not None
            and discount is not None
            and advance_amount is not None
        ):
            if discount < 0 or advance_amount < 0:
                raise ValidationError(
                    'Discount and advance amount cannot be negative.'
                )

            if discount + advance_amount > total_amount:
                raise ValidationError(
                    'Discount and advance amount cannot exceed total amount.'
                )

            pending_amount = (
                total_amount - discount - advance_amount
            )
            cleaned_data['pending_amount'] = pending_amount

            if pending_amount == 0:
                cleaned_data['payment_status'] = 'Paid'
            elif advance_amount > 0 or discount > 0:
                cleaned_data['payment_status'] = 'Partial'
            else:
                cleaned_data['payment_status'] = 'Pending'

        return cleaned_data




class PaymentAdmin(admin.ModelAdmin):
    form = PaymentForm

    def save_model(self, request, obj, form, change):
        from django.utils import timezone

        obj.pending_amount = (
            obj.total_amount - obj.discount - obj.advance_amount
        )

        if obj.pending_amount == 0:
            obj.payment_status = 'Paid'
            if not obj.payment_date:
                obj.payment_date = timezone.now()
        elif obj.advance_amount > 0 or obj.discount > 0:
            obj.payment_status = 'Partial'
            obj.payment_date = None
        else:
            obj.payment_status = 'Pending'
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
        ):
            ready_stage = ProcessingStage.objects.filter(
                order=order,
                stage_name='Ready'
            ).first()

            if not ready_stage or ready_stage.status != 'Completed':
                raise ValidationError(
                    'The Ready stage must be Completed before delivery.'
                )

        return cleaned_data


class DeliveryAdmin(admin.ModelAdmin):
    form = DeliveryForm

    def save_model(self, request, obj, form, change):
        from django.utils import timezone

        order = obj.order

        was_delivered = False

        if change and obj.pk:
            old_delivery = Delivery.objects.filter(
                pk=obj.pk
            ).first()

            if old_delivery:
                was_delivered = (
                    old_delivery.delivery_status.strip().lower()
                    == 'delivered'
                )

        if obj.delivery_status.strip().lower() == 'delivered':
            ready_stage = ProcessingStage.objects.filter(
                order=order,
                stage_name='Ready'
            ).first()

            delivered_stage = ProcessingStage.objects.filter(
                order=order,
                stage_name='Delivered'
            ).first()

            if not ready_stage or ready_stage.status != 'Completed':
                raise ValidationError(
                    'The Ready stage must be Completed before delivery.'
                )

            if not delivered_stage:
                raise ValidationError(
                    'Delivered processing stage was not found for this order.'
                )

            if not obj.delivery_date:
                obj.delivery_date = timezone.now()
        super().save_model(request, obj, form, change)

        if obj.delivery_status.strip().lower() == 'delivered':
            delivered_stage.status = 'Completed'

            if not delivered_stage.started_at:
                delivered_stage.started_at = timezone.now()

            if not delivered_stage.completed_at:
                delivered_stage.completed_at = timezone.now()

            delivered_stage.save()

            if not was_delivered and order.status != 'Delivered':
                order.status = 'Delivered'
                order.save(update_fields=['status'])
            if not Notification.objects.filter(
                user=order.customer.user,
                order=order,
                notification_type='Delivery Update'
            ).exists():
                Notification.objects.create(
                    user=order.customer.user,
                    order=order,
                    message=(
                        f"Your Order #{order.id} "
                        "has been delivered successfully."
                    ),
                    notification_type='Delivery Update'
                )

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
admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Service)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'order_date',
        'expected_date',
        'status',
        'total_amount',
    )
    list_filter = ('status', 'order_date', 'expected_date')
    search_fields = ('customer__name', 'customer__user__username')

admin.site.register(OrderItem)
