from django.test import TestCase, Client
from django.urls import reverse
from carpatianknights.route.models import Route


class TestRouteView(TestCase):

    def setUp(self):
        self.client = Client()
        self.route1 = Route.objects.create(name='test route1', description='some route1 description',
                                           short_description='some short route1 description', complexity=5)

    def test_route_page_GET(self):
        response = self.client.get(reverse('route:route'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'route/route.html')

    def test_route_detail_GET(self):
        response = self.client.get(reverse('route:detail', args=[1, 'test-route1']))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'route/route_detail.html')

    def test_active_tour_page_GET(self):
        response = self.client.get(reverse('route:active_tour_page'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'route/active_tours.html')
