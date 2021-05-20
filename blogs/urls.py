
from django.urls import path
from .views import dashboard, blog


urlpatterns = [
    # path('', blog.home, name='home'),
    path('dashboard/', dashboard.dashboard, name='dashboard'),
    path('dashboard/styles/', dashboard.styles, name='styles'),
]
