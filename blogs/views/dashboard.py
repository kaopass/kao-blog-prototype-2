from django.db.models import Count
from django.views.generic import DeleteView

from blogs.views.blog import resolve_address
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import redirect, render, get_object_or_404
from tldextract import tldextract
from django.utils.text import slugify
from django.utils import timezone

from blogs.forms import StyleForm, BlogForm, PostForm
from blogs.models import Blog, Post


def resolve_subdomain(http_host, blog):
    extracted = tldextract.extract(http_host)
    if extracted.subdomain and extracted.subdomain != blog.subdomain:
        return False
    return True


@login_required
def styles(request):
    blog = get_object_or_404(Blog, user=request.user)

    if not resolve_subdomain(request.META['HTTP_HOST'], blog):
        return redirect(f"{blog.useful_domain()}/dashboard")

    if request.method == "POST":
        form = StyleForm(request.POST, instance=blog)
        if form.is_valid():
            blog_info = form.save(commit=False)
            blog_info.save()
    else:
        form = StyleForm(instance=blog)
    return render(request, 'dashboard/styles.html', {
        'blog': blog,
        'form': form,
    })


@login_required
def dashboard(request):
    try:
        blog = Blog.objects.get(user=request.user)
        if not resolve_subdomain(request.META['HTTP_HOST'], blog):
            return redirect(f"{blog.useful_domain()}/dashboard")

        if request.method == "POST":
            form = BlogForm(request.POST, instance=blog)
            if form.is_valid():
                blog_info = form.save(commit=False)
                blog_info.save()
        else:
            form = BlogForm(instance=blog)
    except Blog.DoesNotExist:
        blog = Blog(
            user=request.user,
            title=f"{request.user.username}'s blog",
            subdomain=slugify(f"{request.user.username}-new"),
            content="Hello World!",
            created_date=timezone.now()
        )
        blog.save()
        form = BlogForm(instance=blog)

    return render(request, 'dashboard/dashboard.html', {
        'form': form,
        'blog': blog,
        'root': blog.useful_domain
    })


@login_required
def posts_edit(request):
    blog = get_object_or_404(Blog, user=request.user)
    if not resolve_subdomain(request.META['HTTP_HOST'], blog):
        return redirect(f"{blog.useful_domain()}/dashboard")

    posts = Post.objects.all()

    return render(request, 'dashboard/posts.html', {
        'posts': posts,
        'blog': blog
    })


@login_required
def post_new(request):
    blog = get_object_or_404(Blog, user=request.user)
    if not resolve_subdomain(request.META['HTTP_HOST'], blog):
        return redirect(f"{blog.useful_domain()}/dashboard")

    if request.method == "POST":
        form = PostForm(request.user, request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.blog = blog
            if not post.published_date:
                post.published_date = timezone.now()
            post.save()
            form.save_m2m()

            return redirect(f"/dashboard/posts/{post.id}/")

    else:
        form = PostForm(request.user)
    return render(request, 'dashboard/post_edit.html', {
        'form': form,
        'blog': blog
    })


@login_required
def post_edit(request, pk):
    blog = get_object_or_404(Blog, user=request.user)
    if not resolve_subdomain(request.META['HTTP_HOST'], blog):
        return redirect(f"{blog.useful_domain()}/dashboard")

    post = get_object_or_404(Post, blog=blog, pk=pk)
    published_date_old = post.published_date
    if request.method == "POST":
        form = PostForm(request.user, request.POST, instance=post)
        if form.is_valid():
            post_new = form.save(commit=False)
            post_new.blog = blog
            # This prevents the resetting of time to 00:00 if same day edit
            if (published_date_old and
                    post_new.published_date and
                    published_date_old.date() == post_new.published_date.date()):
                post_new.published_date = published_date_old
            if not post_new.published_date:
                post_new.published_date = timezone.now()
            post_new.save()
            form.save_m2m()
    else:
        form = PostForm(request.user, instance=post)

    return render(request, 'dashboard/post_edit.html', {
        'form': form,
        'blog': blog,
        'post': post,
    })


class PostDelete(DeleteView):
    model = Post
    success_url = '/dashboard/posts'
