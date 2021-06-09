
from django.urls import path
from .views import dashboard, blog, emailer

urlpatterns = [
    path('', blog.home, name='home'),
    path('dashboard/', dashboard.dashboard, name='dashboard'),
    path('dashboard/styles/', dashboard.styles, name='styles'),
    path('dashboard/posts/', dashboard.posts_edit, name='post'),
    path('dashboard/posts/new/', dashboard.post_new, name='post_new'),
    path('dashboard/posts/<pk>/', dashboard.post_edit, name='post_edit'),
    path('dashboard/posts/<pk>/delete/', dashboard.PostDelete.as_view(),
         name='post_delete'),
    path('<slug>/', blog.post, name='post'),
    path('dashboard/subscribers/', emailer.subscribers, name='subscribers'),
    path('dashboard/export_emails/', dashboard.export_emails, name='export_emails'),

]
