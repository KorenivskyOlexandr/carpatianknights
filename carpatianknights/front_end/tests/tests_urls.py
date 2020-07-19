from django.test import SimpleTestCase
from django.urls import resolve
from carpatianknights.front_end.views import main_page


class TestsUrls(SimpleTestCase):
    def test_main_page_url_is_resolves(self):
        self.assertEquals(resolve('/').func, main_page)
