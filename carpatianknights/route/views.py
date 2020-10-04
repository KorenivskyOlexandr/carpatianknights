from django.shortcuts import render
from .services import get_active_tour_list, get_route_list, get_route_detail


def active_tour_page(request):
    active_tour_list = get_active_tour_list()
    return render(request, 'route/active_tours.html', {'active_tour_list': active_tour_list})


def route_page(request):
    route = get_route_list()
    return render(request, 'route/route.html', {'route_list': route})


def route_detail(request, id, slug):
    route = get_route_detail(id, slug)
    return render(request, 'route/route_detail.html', {'route': route})
