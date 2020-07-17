from django.test import SimpleTestCase
from carpatianknights.news.forms import EmailPostForm, CommentForm, SearchForm


class TestForms(SimpleTestCase):

    def test_email_post_form_valid_data(self):
        form = EmailPostForm(data={
            'name': 'test name',
            'email': 'test@testemail.com',
            'to': 'to_test@testemail.com',
            'comments': 'test comment to post'
        })

        self.assertTrue(form.is_valid())

    def test_email_post_form_no_data(self):
        form = EmailPostForm(data={})

        self.assertFalse(form.is_valid())

    def test_comment_form_valid_data(self):
        form = CommentForm(data={
            'name': 'test name',
            'email': 'test@testemail.com',
            'body': 'test body comment'
        })

        self.assertTrue(form.is_valid())

    def test_comment_form_no_data(self):
        form = CommentForm(data={})

        self.assertFalse(form.is_valid())

    def test_search_form_valid_data(self):
        form = SearchForm(data={
            'query': 'test query'
        })

        self.assertTrue(form.is_valid())

    def test_search_form_no_data(self):
        form = SearchForm(data={})

        self.assertFalse(form.is_valid())
