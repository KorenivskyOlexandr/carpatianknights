from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class Photo(models.Model):
    image = models.ImageField()
    title = models.CharField(max_length=100)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.image = self.compress_image()
        super(Photo, self).save(*args, **kwargs)

    def compress_image(self):
        image_temproary = Image.open(self.image)
        outputIoStream = BytesIO()
        image_temproary.resize((1920, 1080))
        image_temproary.save(outputIoStream, format='JPEG', quality=50)
        outputIoStream.seek(0)
        uploaded_image = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % self.image.name.split('.')[0],
                                              'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploaded_image
