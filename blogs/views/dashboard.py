from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import render, get_object_or_404
from tldextract import tldextract

from blogs.forms import StyleForm
from blogs.models import Blog


# def resolve_subdomain(http_host, blog):
#     extracted = tldextract.extract(http_host)
#     if extracted.subdomain and extracted.subdomain != blog.subdomain:
#         return False
#     return True

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