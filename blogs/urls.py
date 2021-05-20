from django.urls import path

from .views import blog

urlpatterns = [
    path('', blog.home, name='home'),
]
