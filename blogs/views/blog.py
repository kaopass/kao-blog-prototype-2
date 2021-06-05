import tldextract
from django.contrib.sites.models import Site
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from ipaddr import client_ip

from blogs.helpers import get_nav, get_posts

from blogs.models import Blog, Post, Upvote


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


def get_post(all_posts, slug):
    try:
        return list(filter(lambda post: post.slug == slug, all_posts))[0]
    except IndexError:
        raise Http404("No Post matches the given query.")


def post(request, slug):
    blog = get_object_or_404(Blog, user=request.user)

    ip_address = client_ip(request)

    if request.method == "POST":
        if request.POST.get("pk", ""):
            # Upvoting
            pk = request.POST.get("pk", "")
            post = get_object_or_404(Post, pk=pk)
            posts_upvote_dupe = post.upvote_set.filter(ip_address=ip_address)
            if len(posts_upvote_dupe) == 0:
                upvote = Upvote(post=post, ip_address=ip_address)
                upvote.save()

    if request.GET.get('preview'):
        all_posts = blog.post_set.annotate(
            upvote_count=Count('upvote')).all().order_by('-published_date')
    else:
        all_posts = blog.post_set.annotate(
            upvote_count=Count('upvote')).filter(publish=True).order_by('-published_date')

    post = get_post(all_posts, slug)

    upvoted = False
    for upvote in post.upvote_set.all():
        if upvote.ip_address == ip_address:
            upvoted = True

    return render(
        request,
        'post.html',
        {
            'blog': blog,
            'content': post.content,
            'post': post,
            'root': blog.useful_domain(),
            'upvoted': upvoted

        }
    )
