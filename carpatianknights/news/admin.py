from django.contrib import admin
from .models import Post, Comment, Photo, PhotoToPost, PhotoToRoutes, Route, ActiveRoute, Tour


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


admin.site.register(ActiveRoute)
admin.site.register(PhotoToPost)


class PhotoToRoutesInlane(admin.StackedInline):
    model = PhotoToRoutes


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'complexity')
    list_filter = ('name', 'slug', 'complexity')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PhotoToRoutesInlane]


admin.site.register(PhotoToRoutes)
admin.site.register(Tour)
admin.site.register(Photo)
