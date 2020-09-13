import os
from django.core.exceptions import ValidationError
from django.test import TestCase
from carpatianknights.route.models import Route, ActiveRoute, Tour
from carpatianknights.account.models import Profile
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from datetime import date, timedelta
from django.core import mail


class BaseModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(BaseModelTestCase, cls).setUpClass()
        cls.test_image = SimpleUploadedFile(name='test_image.jpg',
                                            content=open(
                                                os.path.join(settings.BASE_DIR, 'dist/') + 'images/test_image.jpg', 'rb').read(),
                                            content_type='image/jpeg')
        cls.route1 = Route.objects.create(name='test route1', description='some route1 description',
                                          short_description='some short route1 description', complexity=5,
                                          title_img=cls.test_image)
        cls.active_route1 = ActiveRoute.objects.create(routes_id=cls.route1, start_day=date.today(),
                                                       stop_day=(date.today() + timedelta(days=5)),
                                                       leader='route leader', status=True, is_full=False, free_places=9)
        cls.active_route2 = ActiveRoute.objects.create(routes_id=cls.route1, start_day=date.today(),
                                                       stop_day=(date.today() + timedelta(days=5)),
                                                       leader='route leader', status=True, is_full=False, free_places=9)
        cls.user1 = Profile.objects.create(
            user=User.objects.create(username='user1', email='user1@testemail.com', password='testPassw0rd'),
            phone_number=999999999, date_of_birth=date(1997, 8, 25))
        cls.tour1 = Tour.objects.create(user_id=cls.user1.user, active_route_id=cls.active_route1, status=False)
        cls.tour2 = Tour(user_id=cls.user1.user, active_route_id=cls.active_route2, status=False)


class TestRouteModels(BaseModelTestCase):

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


class TestActiveRouteModel(BaseModelTestCase):

    def test_add_user(self):
        self.assertEquals(self.active_route1.free_places, 9)
        self.active_route1.add_user()
        self.assertEquals(self.active_route1.free_places, 8)
        self.active_route1.free_places = 0
        self.assertRaises(ValidationError, self.active_route1.add_user)

    def test_remove_user(self):
        self.active_route1.free_places = 0
        self.active_route1.save()
        self.assertEquals(self.active_route1.free_places, 0)
        self.active_route1.remove_user()
        self.assertEquals(self.active_route1.free_places, 1)

    def test_auto_full_when_saving(self):
        self.assertEquals(self.active_route1.free_places, 0)
        self.active_route1.save()
        self.assertEquals(self.active_route1.is_full, True)
        self.active_route1.free_places = 9
        self.active_route1.save()
        self.assertEquals(self.active_route1.is_full, False)

    def test_date_validation_on_save(self):
        self.assertGreater(self.active_route2.stop_day, self.active_route2.start_day)
        self.active_route2.start_day = date.today() - timedelta(days=1)
        self.assertRaises(ValidationError, self.active_route2.save)
        self.active_route2.stop_day = self.active_route2.start_day - timedelta(days=1)
        self.assertRaises(ValidationError, self.active_route2.save)


class TestTourModel(BaseModelTestCase):

    def test_create_tour(self):
        self.assertEquals(Tour.objects.count(), 1)

    def test_user_notification(self):
        self.tour1.status = True
        self.tour1.save()
        first_message = mail.outbox[0]
        self.assertEquals(first_message.subject, 'Карпатські Відчайдухи')
        self.assertEquals(first_message.from_email, 'carpatianknights@gmail.com')
        self.assertEquals(first_message.recipients(), [self.user1.user.email])

    def test_admin_notification(self):
        self.tour2.save()
        first_message = mail.outbox[0]
        self.assertEquals(first_message.subject, 'Карпатські Відчайдухи')
        self.assertEquals(first_message.from_email, 'carpatianknights@gmail.com')
        self.assertEquals(first_message.recipients(), ['carpatianknights@ukr.net', 's5a5s5h5a5@ukr.net'])

    def test_change_free_place_when_accepting_user(self):
        self.assertEquals(self.active_route2.free_places, 9)
        self.tour2.status = True
        self.tour2.save()
        self.assertEquals(self.active_route2.free_places, 8)

    def test_change_free_place_when_deleting_user(self):
        self.assertEquals(self.active_route2.free_places, 8)
        self.tour2.delete()
        self.assertEquals(self.active_route2.free_places, 9)
