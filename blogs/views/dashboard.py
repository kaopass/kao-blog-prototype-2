from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def styles(request):
    print("Hello")