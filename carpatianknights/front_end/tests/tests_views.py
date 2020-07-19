from django.test import TestCase, Client


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_main_page_GET(self):
        response = self.client.get('/')

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
