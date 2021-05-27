
from django.urls import path
from .views import dashboard, blog


urlpatterns = [
    path('', blog.not_found, name='home'),
    path('dashboard/', dashboard.dashboard, name='dashboard'),
    path('dashboard/styles/', dashboard.styles, name='styles'),
    path('dashboard/posts/', dashboard.posts_edit, name='post'),
    path('dashboard/posts/new/', dashboard.post_new, name='post_new'),
    path('dashboard/posts/<pk>/', dashboard.post_edit, name='post_edit'),
    path('dashboard/posts/<pk>/delete/', dashboard.PostDelete.as_view(),
         name='post_delete'),
]
