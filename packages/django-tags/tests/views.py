from django.views.generic.list import ListView

from tags.views import TagListMixin

from .models import Food


class FoodTagListView(TagListMixin, ListView):
    model = Food