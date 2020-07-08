from django.test import SimpleTestCase
from django.urls import reverse, resolve
from carpatianknights.news.views import post_detail, post_list


class TestsUrls(SimpleTestCase):
    def test_post_list_url_is_resolves(self):
        url = reverse('news:post_list')
        self.assertEquals(resolve(url).func, post_list)

    def test_post_detail_url_is_resolves(self):
        url = reverse('news:post_detail', args=['2020', '5', '15', 'post'])
        self.assertEquals(resolve(url).func, post_detail)

    def test_post_list_by_tag_url_is_resolves(self):
        url = reverse('news:post_list_by_tag', args=['post'])
        self.assertEquals(resolve(url).func, post_list)
