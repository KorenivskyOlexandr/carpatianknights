from django.shortcuts import get_object_or_404
from .models import ActiveRoute, Route
from datetime import date


def get_active_tour_list():
    return ActiveRoute.objects.filter(status=True, is_full=False, start_day__gte=date.today())


def get_route_list():
    return Route.objects.all()


def get_route_detail(id, slug):
    return get_object_or_404(Route, id=id, slug=slug)
