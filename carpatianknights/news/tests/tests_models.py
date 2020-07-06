from django.test import TestCase
from carpatianknights.news.models import Post, Comment
from django.contrib.auth.models import User
from django.urls import reverse


class TestModels(TestCase):

    def setUp(self):
        self.post1 = Post.objects.create(
            title='test post1',
            author=User.objects.create(),
            body='test text to post1',
            status='published'

        )

    def test_post_is_assigned_slug_on_creation(self):
        self.assertEquals(self.post1.slug, self.post1.title.replace(' ', '-'))

    def test_post_get_absolute_url(self):
        self.assertEquals(self.post1.get_absolute_url(), reverse('news:post_detail', args=[self.post1.publish.year,
                                                                                           self.post1.publish.month,
                                                                                           self.post1.publish.day,
                                                                                           self.post1.slug]))

    def test_creation_comment(self):
        self.comment1 = Comment.objects.create(post=self.post1, name='test comment', email='test@mail.com',
                                               body='some comment text')
        self.assertEquals(self.post1.comments.count(), 1)
        self.assertEquals(self.comment1.__str__(), 'Comment by {} on {}'.format(self.comment1.name, self.post1.title))
