from django.test import TestCase
from carpatianknights.account.models import Profile
from django.contrib.auth.models import User
from datetime import date
from django.core.exceptions import ValidationError


class BaseModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(BaseModelTestCase, cls).setUpClass()
        cls.user1 = User.objects.create(username='user1', email='user1@testemail.com', password='testPassw0rd')
        cls.user2 = User.objects.create(username='user2', email='user2@testemail.com', password='testPassw0rd')
        cls.user3 = User.objects.create(username='user3', email='user3@testemail.com', password='testPassw0rd')

        cls.profile1 = Profile(
            user=cls.user1,
            phone_number=999999999, date_of_birth=date(1997, 8, 25))
        cls.profile2 = Profile(
            user=cls.user2,
            phone_number=999999998, date_of_birth=date(2010, 8, 25))
        cls.profile3 = Profile(
            user=cls.user2,
            phone_number=999999999, date_of_birth=date(2000, 8, 25))


class TestAccountModels(BaseModelTestCase):

    def test_creating_profile(self):
        self.profile1.save()
        self.assertEquals(Profile.objects.count(), 1)
        self.assertEquals(self.profile1.user_rang, 0)
        self.assertEquals(self.profile1.date_of_registration, date.today())

    def test_valid_date_of_birth(self):
        self.assertRaises(ValidationError, self.profile2.full_clean)
