from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from .helpers import delete_domain, add_new_domain


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    subdomain = models.SlugField(max_length=100, unique=True)
    domain = models.CharField(max_length=128, blank=True, null=True)
    content = models.TextField(blank=True)
    external_stylesheet = models.CharField(max_length=255, blank=True)
    custom_styles = models.TextField(blank=True)
    favicon = models.CharField(max_length=4, default="📣")

    reviewed = models.BooleanField(default=False)
    upgraded = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)

    def useful_domain(self):
        if self.domain:
            return f'http://{self.domain}'
        else:
            return f'http://{self.subdomain}.{Site.objects.get_current().domain}'

    def __str__(self):
        return f'{self.title} ({self.useful_domain()})'

    def save(self, *args, **kwargs):
        if self.pk:
            if self.domain:
                self.domain = self.domain.lower()
            old_domain = Blog.objects.get(pk=self.pk).domain
            if old_domain != self.domain:
                delete_domain(old_domain)
                if self.domain:
                    add_new_domain(self.domain)

        self.subdomain = self.subdomain.lower()

        return super(Blog, self).save(*args, **kwargs)


@receiver(pre_delete, sender=Blog, dispatch_uid='blog_delete_signal')
def delete_blog_receiver(sender, instance, using, **kwargs):
    if instance.domain:
        print("Deleting domain from Heroku")
        delete_domain(instance.domain)


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100)
    published_date = models.DateTimeField(blank=True)
    publish = models.BooleanField(default=True)
    content = models.TextField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = self.slug.lower()
        super(Post, self).save(*args, **kwargs)
