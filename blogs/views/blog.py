import tldextract
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404, render

from blogs.helpers import get_nav, get_posts

from blogs.models import Blog


def resolve_address(request):
    http_host = request.META['HTTP_HOST']
    sites = Site.objects.all()
    if any(http_host == site.domain for site in sites):
        # HomePage
        return None
    elif any(site.domain in http_host for site in sites):
        # Sub domained blog
        return get_object_or_404(Blog, subdomain=tldextract.extract(http_host).subdomain, blocked=False)
    else:
        # Custom domain blog
        return get_object_or_404(Blog, domain=http_host, blocked=False)


def home(request):
    blog = resolve_address(request)
    if not blog:
        return render(request, 'landing.html')

    all_posts = blog.post_set.filter(publish=True).order_by('-published_date')

    return render(
        request,
        'home.html',
        {
            'blog': blog,
            'content': blog.content,
            'posts': get_posts(all_posts),
            'nav': get_nav(all_posts),
            'root': blog.useful_domain(),
        })


def not_found(request, *args, **kwargs):
    return render(request, '404.html', status=404)
