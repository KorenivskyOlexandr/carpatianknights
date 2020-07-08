from django.core.exceptions import ValidationError
from django.test import TestCase
from carpatianknights.route.models import Route, ActiveRoute, Tour
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings


class TestRouteModels(TestCase):

    def setUp(self):
        self.test_image = SimpleUploadedFile(name='test_image.jpg',
                                             content=open(
                                                 settings.STATIC_ROOT + 'images/test_image.jpg', 'rb').read(),
                                             content_type='image/jpeg')
        self.route1 = Route.objects.create(name='test route1', description='some route1 description',
                                           short_description='some short route1 description', complexity=5,
                                           title_img=self.test_image)

    def test_route_is_assigned_slug_on_creation(self):
        self.assertEquals(self.route1.slug, self.route1.name.replace(' ', '-'))

    def test_route_complexity_creation(self):
        self.route1.complexity = 123
        self.assertRaises(ValidationError, self.route1.full_clean)
        self.route1.complexity = -100
        self.assertRaises(ValidationError, self.route1.full_clean)
        self.route1.complexity = 5

    def test_route_get_absolute_url(self):
        self.assertEquals(self.route1.get_absolute_url(),
                          reverse('route:detail', args=[self.route1.id, self.route1.slug]))

    def test_route_title_image_resize(self):
        self.assertGreater(self.test_image.size, self.route1.title_img.size)
