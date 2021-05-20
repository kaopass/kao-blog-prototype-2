from blogs.views.blog import resolve_address
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import redirect, render, get_object_or_404
from tldextract import tldextract
from django.utils.text import slugify
from django.utils import timezone

from blogs.forms import StyleForm, BlogForm
from blogs.models import Blog


def resolve_subdomain(http_host, blog):
    extracted = tldextract.extract(http_host)
    if extracted.subdomain and extracted.subdomain != blog.subdomain:
        return False
    return True


@login_required
def styles(request):
    # blog = get_object_or_404(Blog, user=request.user)

    # if not resolve_subdomain(request.META['HTTP_HOST'], blog):
    #     return redirect(f"{blog.useful_domain()}/dashboard")

    if request.method == "POST":
        form = StyleForm(request.POST)
        if form.is_valid():
            blog_info = form.save(commit=False)
            blog_info.save()
    else:
        form = StyleForm()
    return render(request, 'dashboard/styles.html', {
        # 'blog': blog,
        'form': form,
    })


@login_required
def dashboard(request):
    try:
        blog = Blog.objects.get(user=request.user)
        if not resolve_subdomain(request.META['HTTP_HOST'], blog):
            return redirect(f"{blog.useful_domain()}/dashboard")

        if request.method == "POST":
            pass
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
