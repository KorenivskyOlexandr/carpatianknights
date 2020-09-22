from django.apps import AppConfig


class RouteConfig(AppConfig):
    name = 'carpatianknights.route'

    def ready(self):
        import carpatianknights.route.signals