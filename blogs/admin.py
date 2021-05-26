from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from django.utils.html import format_html
from django.db.models import Count

from .models import Blog

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    def subdomain_url(self, obj):
        blog = Blog.objects.get(user=obj)
        return format_html(
            "<a href='{url}' target='_blank>{url}</a>",
            url={blog.useful_domain()}
        )
    subdomain_url.short_description = "Subdomain"

    list_display = ('email', 'subdomain_url', 'is_active', 'is_staff', 'date_joined')
    ordering = ('-date_joined',)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

