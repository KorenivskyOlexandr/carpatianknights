from django.test import SimpleTestCase
from django.urls import reverse, resolve
from carpatianknights.route.views import active_tour_page, route_page, route_detail


class TestsUrls(SimpleTestCase):
    def test_route_page_url_is_resolves(self):
        url = reverse('route:route')
        self.assertEquals(resolve(url).func, route_page)

    def test_active_tour_page_url_is_resolves(self):
        url = reverse('route:active_tour_page')
        self.assertEquals(resolve(url).func, active_tour_page)

    def test_route_detail_url_is_resolves(self):
        url = reverse('route:detail', args=['1', 'route'])
        self.assertEquals(resolve(url).func, route_detail)
