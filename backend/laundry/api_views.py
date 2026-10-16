
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Service


@api_view(['GET'])
def services_api(request):
    services = Service.objects.all()

    data = [
        {
            'id': service.id,
            'name': service.service_name,
            'price': str(service.price_per_item),
            'description': service.description,
        }
        for service in services
    ]

    return Response(data)
