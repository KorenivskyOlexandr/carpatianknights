from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('carpatianknights.front_end.urls', namespace='front_end')),
    path('news/', include('carpatianknights.news.urls', namespace='news')),
    path('account/', include('carpatianknights.account.urls')),
    path('route/', include('carpatianknights.route.urls', namespace='route')),
    path('admin/', admin.site.urls),
    # path('social-auth/', include('social_django.urls', namespace='social')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
