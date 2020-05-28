from django.shortcuts import render, get_object_or_404
from .models import ActiveRoute, Route


def active_tour_page(request):
    active_tour_list = ActiveRoute.objects.filter(status=True, is_full=False)
    return render(request, 'route/active_tours.html', {'active_tour_list': active_tour_list})


def route_page(request):
    route = Route.objects.all()
    return render(request, 'route/route.html', {'route_list': route})


def route_detail(request, id, slug):
    route = get_object_or_404(Route, id=id, slug=slug)
    return render(request, 'route/route_detail.html', {'route': route})
