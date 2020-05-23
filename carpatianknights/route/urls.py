from django.urls import path
from . import views

app_name = 'route'
urlpatterns = [
    path('', views.route_page, name='route'),
    path('active_tours/', views.active_tour_page, name='active_tour_page'),
    path('detail/<int:id>/<slug:slug>/', views.route_detail, name='detail'),
]
