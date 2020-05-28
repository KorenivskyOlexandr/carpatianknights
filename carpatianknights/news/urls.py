from django.urls import path
from . import views
# from .feeds import LatestPostsFeed

app_name = 'news'
urlpatterns = [
    # post views
    path('', views.main_page),
    path('news/', views.post_list, name='post_list'),
    # path('', views.PostListView.as_view(), name='post_list'),
    path('news/<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail, name='post_detail'),
    path('active_tours/', views.active_tour_page, name='active_tour_page'),
    path('route/', views.route_page, name='route'),
    path('detail/<int:id>/<slug:slug>/', views.route_detail, name='detail'),
    # path('news/<int:post_id>/share/', views.post_share, name='post_share'),
    # path('news/tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    # path('news/feed/', LatestPostsFeed(), name='post_feed'),
    # path('news/search/', views.post_search, name='post_search'),
]
