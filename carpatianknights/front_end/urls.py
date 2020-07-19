from django.urls import path
from . import views

app_name = 'front_end'
urlpatterns = [
    path('', views.main_page),
]
