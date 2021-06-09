import re

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
import djqscsv

from blogs.models import Subscriber, Blog
from blogs.views.dashboard import resolve_subdomain


@login_required
def subscribers(request):
    blog = get_object_or_404(Blog, user=request.user)
    if not resolve_subdomain(request.META['HTTP_HOST'], blog):
        return redirect(f"{blog.useful_domain()}/dashboard")

    if request.GET.get("delete", ""):
        Subscriber.objects.filter(blog=blog, pk=request.GET.get("delete", "")).delete()

    subscribers = Subscriber.objects.filter(blog=blog)

    if request.GET.get("export", ""):
        subscribers = subscribers.values('email_address', 'subscribed_date')
        return djqscsv.render_to_csv_response(subscribers)

    if request.POST.get("email_addresses", ""):
        email_addresses = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", request.POST.get("email_addresses", ""))

        for email in email_addresses:
            Subscriber.objects.get_or_create(blog=blog, email_address=email)

    return render(request, "dashboard/subscribers.html", {
        "blog": blog,
        "subscribers": subscribers,
    })

