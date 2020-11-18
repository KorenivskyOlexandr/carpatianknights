from django.shortcuts import render
from .services import get_post_list_context, get_post


def post_list_view(request, tag_slug=None):
    return render(request, 'news/post/list.html', get_post_list_context(request, tag_slug))


def post_detail_view(request, year, month, day, post):
    post = get_post(year, month, day, post)
    return render(request, 'news/post/detail.html', {'post': post})
