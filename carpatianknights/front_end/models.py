from django.db import models
from .services import compress_image
from django.utils.text import slugify


class Photo(models.Model):
    image = models.ImageField()
    title = models.CharField(max_length=100)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.image = compress_image(self.image)
        super(Photo, self).save(*args, **kwargs)


class File(models.Model):
    file = models.FileField(upload_to='files/')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(File, self).save(*args, **kwargs)
