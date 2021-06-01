from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from django.utils.html import format_html, escape
from django.db.models import Count
from blogs.helpers import root

from django.urls import reverse

from .models import Blog, Post


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


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return Blog.objects.annotate(post_count=Count('post'))

    def post_count(self, obj):
        return obj.post_count

    # TODO: https://timonweb.com/django/how-to-sort-django-admin-list-column-by-a-value-from-a-related-model/
    post_count.short_description = ('Post count')
    post_count.admin_order_field = "posts_count"

    def domain_url(self, obj):
        if not obj.domain:
            return ''
        return format_html(
            "<a href='http://{url}' target='_blank'>{url}</a>",
            url=obj.domain
        )

    domain_url.short_description = "Domain url"
    domain_url.admin_order_field = 'domain'

    def subdomain_url(self, obj):
        return format_html(
            "<a href='http://{url}' target='_blank'>{url}</a>",
            url=root(obj.subdomain))

    subdomain_url.short_description = "Subomain"

    def user_link(self, obj):
        return format_html('<a href="{url}">{username}</a>',
                           url=reverse("admin:auth_user_change", args=(obj.user.id,)),
                           username=escape(obj.user))

    user_link.allow_tags = True
    user_link.short_description = "User"

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = "Email"

    list_display = (
        'title',
        'reviewed',
        'upgraded',
        'blocked',
        'subdomain_url',
        'domain_url',
        'post_count',
        'user_link',
        'user_email',
        'created_date')

    search_fields = ('title', 'subdomain', 'domain', 'user__email')
    ordering = ('-created_date',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return Post.objects.annotate(upvote_count=Count('upvote'))

    def upvote_count(self, obj):
        return obj.upvote_count

    upvote_count.short_description = ('Upvotes')


list_display = ('title', 'blog', 'upvote_count', 'published_date')
search_fields = ('title', 'blog__title')
ordering = ('-published_date',)

