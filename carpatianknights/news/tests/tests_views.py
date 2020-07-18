from django.test import TestCase, Client
from django.urls import reverse
from carpatianknights.news.models import Post
from carpatianknights.account.models import Profile
from django.contrib.auth.models import User
from datetime import date
from django.db import transaction


class BaseModelTestCase(TestCase):

    @classmethod
    @transaction.atomic
    def setUpClass(cls):
        super(BaseModelTestCase, cls).setUpClass()
        cls.client = Client()
        cls.user1 = Profile.objects.create(
            user=User.objects.create(username='user1', email='user1@testemail.com', password='testPassw0rd'),
            phone_number=999999999, date_of_birth=date(1997, 8, 25))
        for i in range(30):
            post = Post.objects.create(
                title='testing post{}'.format(i),
                author=cls.user1.user,
                body='test text to post{}'.format(i),
                status='published'
            )
            post.tags.add("post" if i % 2 == 0 else "test")
            post.save()


class TestNewsView(BaseModelTestCase):

    def test_post_list_GET(self):
        response = self.client.get(reverse('news:post_list'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/post/list.html')

    def test_post_list_by_tag_GET(self):
        response = self.client.get(reverse('news:post_list_by_tag', args=['post']))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/post/list.html')

    def test_post_detail_GET(self):
        self.post1 = Post.objects.get(id=1)
        response = self.client.get(reverse('news:post_detail', args=[self.post1.publish.year,
                                                                     self.post1.publish.month,
                                                                     self.post1.publish.day,
                                                                     self.post1.slug]))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/post/detail.html')
