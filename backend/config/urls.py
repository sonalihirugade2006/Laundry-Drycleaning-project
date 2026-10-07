from django.contrib import admin
from django.urls import path
from laundry.views import home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
]