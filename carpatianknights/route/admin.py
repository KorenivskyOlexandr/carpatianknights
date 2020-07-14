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


@admin.register(ActiveRoute)
class ActiveRouteAdmin(admin.ModelAdmin):
    list_display = ('routes_id', 'start_day', 'stop_day', 'leader', 'status', 'is_full', 'free_places')
    list_filter = ('routes_id', 'start_day', 'stop_day', 'leader', 'status', 'is_full', 'free_places')
    search_fields = ('routes_id', 'start_day', 'stop_day', 'leader', 'status', 'is_full', 'free_places')


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('get_user_full_name', 'active_route_id', 'get_start_day', 'get_stop_day', 'status')
    list_filter = ('active_route_id', 'status')
    search_fields = ('get_user_full_name', 'active_route_id', 'get_start_day', 'get_stop_day', 'status')

    def get_user_full_name(self, obj):
        return obj.user_id.get_full_name()

    def get_start_day(self, obj):
        return obj.active_route_id.start_day

    def get_stop_day(self, obj):
        return obj.active_route_id.stop_day

    get_user_full_name.admin_order_field = 'user_id'  # Allows column order sorting
    get_user_full_name.short_description = 'Відчайдуха'  # Renames column head
    get_start_day.short_description = 'Дата початку'
    get_stop_day.short_description = 'Дата Закінчення'


admin.site.register(PhotoToRoutes)
