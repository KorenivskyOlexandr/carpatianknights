from django.contrib import admin
from .models import PhotoToRoutes, Route, ActiveRoute, Tour


class PhotoToRoutesInlane(admin.StackedInline):
    model = PhotoToRoutes


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'complexity')
    list_filter = ('name', 'slug', 'complexity')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PhotoToRoutesInlane]


admin.site.register(ActiveRoute)
admin.site.register(PhotoToRoutes)
admin.site.register(Tour)
