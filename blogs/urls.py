
from django.urls import path
from .views import dashboard


urlpatterns = [
    path('dashboard/styles/', dashboard.styles, name='styles'),
]
