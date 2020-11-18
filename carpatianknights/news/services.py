from django.shortcuts import get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import CommentForm
from taggit.models import Tag
from django.db.models import Count
from .filters import PostFilter


def get_post_list_context(request, tag_slug):
    if tag_slug:
        tag = get_tag(tag_slug)
        object_list = get_post_object_list().filter(tags__in=[tag])
    else:
        tag = None
        object_list = get_post_object_list()
    page = request.GET.get('page')
    post_filter = PostFilter(request.GET, queryset=object_list)
    posts = get_posts_paginator_list(post_filter.qs, page)
    return {'page': page, 'posts': posts, 'tag': tag, 'post_filter': post_filter}


def get_post_object_list():
    return Post.published.all()


def get_tag(tag_slug):
    return get_object_or_404(Tag, slug=tag_slug)


def get_posts_paginator_list(posts_list, page):
    paginator = Paginator(posts_list, 10)  # По 10 статтей на кажній сторінці.
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return posts


def get_post(year, month, day, post):
    return get_object_or_404(Post, slug=post, status='published', publish__year=year,
                             publish__month=month, publish__day=day)

# def get_comment_to_post(post, request):
#     # Список активных комментариев для этой статьи.
#     comments = post.comments.filter(active=True)
#     new_comment = None
#     comment_form = None
#     if request.method == 'POST':
#

# def create_comment(post, request):
#     comment_form = CommentForm(data=request.POST)
#     if comment_form.is_valid():
#         # Создаем комментарий, но пока не сохраняем в базе данных.
#         new_comment = comment_form.save(commit=False)
#         # Привязываем комментарий к текущей статье.
#         new_comment.post = post
#         # Сохраняем комментарий в базе данных.
#         new_comment.save()
#     else:
#         comment_form = CommentForm()

# def get_similar_post(post):
#     post_tags_ids = post.tags.values_list('id', flat=True)
#     similar_posts = Post.published.filter(tags__in=post_tags_ids) \
#         .exclude(id=post.id)
#     similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
#                         .order_by('-same_tags', '-publish')[:4]
#     return similar_posts

# def post_search(request):
#     form = SearchForm()
#     query = None
#     results = []
#     if 'query' in request.GET:
#         form = SearchForm(request.GET)
#     if form.is_valid():
#         query = form.cleaned_data['query']
#     # search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
#     # search_query = SearchQuery(query)
#     results = Post.objects.annotate(
#         similarity=TrigramSimilarity('title', query),
#     ).filter(similarity__gt=0.3).order_by('-similarity')
#     return render(request, 'news/post/search.html', {'form': form,
#                                                      'query': query,
#                                                      'results': results})
