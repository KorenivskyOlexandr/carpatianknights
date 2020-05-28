from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment, ActiveRoute, Photo, Route
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
# from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .forms import EmailPostForm, CommentForm, SearchForm
# from django.contrib.postgres.search import TrigramSimilarity
from taggit.models import Tag
from django.db.models import Count
import datetime


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 10
    template_name = 'news/post/list.html'


def main_page(request):
    year = datetime.datetime.now()
    images_list = Photo.objects.filter(title="gallery")  # в слайдер попадають стиснені фотографігі з title="gallery"
    return render(request, 'main.html', {"year": year, "images": images_list})


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 10)  # По 10 статтей на каждой странице.
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, возвращаем первую страницу.
        posts = paginator.page(1)
    except EmptyPage:
        # Если номер страницы больше, чем общее количество страниц, возвращаем последнюю.
        posts = paginator.page(paginator.num_pages)
    return render(request, 'news/post/list.html', {'page': page, 'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year,
                             publish__month=month, publish__day=day)
    # Список активных комментариев для этой статьи.
    comments = post.comments.filter(active=True)
    new_comment = None
    comment_form = None
    if request.method == 'POST':
        # Пользователь отправил комментарий.
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Создаем комментарий, но пока не сохраняем в базе данных.
            new_comment = comment_form.save(commit=False)
            # Привязываем комментарий к текущей статье.
            new_comment.post = post
            # Сохраняем комментарий в базе данных.
            new_comment.save()
        else:
            comment_form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids) \
        .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
        .order_by('-same_tags', '-publish')[:4]
    return render(request, 'news/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form,
                                                     'similar_posts': similar_posts})


def post_share(request, post_id):
    # отримання статті по ідентифікатору
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == "POST":
        # форма була відправлена на зберігання
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.changed_data
            # ... відправка електронного листа
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "' \
                      '{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:' \
                      '{}'.format(post.title, post_url,
                                  cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
        else:
            return HttpResponse(u'Куда прёшь?', status_code=400)
    else:
        form = EmailPostForm()
        return render(request, 'news/post/share.html',
                      {'post': post, 'form': form, 'sent': sent})


def active_tour_page(request):
    active_tour_list = ActiveRoute.objects.filter(status=True, is_full=False)
    return render(request, 'tour/active_tours.html', {'active_tour_list': active_tour_list})


def route_page(request):
    route = Route.objects.all()
    return render(request, 'tour/route.html', {'route_list': route})


def route_detail(request, id, slug):
    route = get_object_or_404(Route, id=id, slug=slug)
    return render(request, 'tour/route_detail.html', {'route': route})


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
