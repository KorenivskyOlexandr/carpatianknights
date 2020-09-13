import os
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from carpatianknights.front_end.models import Photo


class TestModels(TestCase):

    def setUp(self):
        self.test_image = SimpleUploadedFile(name='test_image.jpg',
                                             content=open(
                                                 os.path.join(settings.BASE_DIR, 'dist/') + 'images/test_image.jpg',
                                                 'rb').read(),
                                             content_type='image/jpeg')
        self.photo1 = Photo.objects.create(image=self.test_image, title='test1')

    def test_creation_photo(self):
        self.assertEquals(Photo.objects.count(), 1)

    def test_photo_str(self):
        self.assertEquals(str(self.photo1), 'test1')

    def test_photo_image_resize(self):
        self.assertGreater(self.test_image.size, self.photo1.image.size)
