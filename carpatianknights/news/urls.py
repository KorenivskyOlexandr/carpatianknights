from django.urls import path
from . import views

app_name = 'news'
urlpatterns = [
    path('', views.post_list_view, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail_view, name='post_detail'),
    path('tag/<slug:tag_slug>/', views.post_list_view, name='post_list_by_tag'),
    # path('news/search/', views.post_search, name='post_search'),
]
